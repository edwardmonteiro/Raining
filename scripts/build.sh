#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
SDK_ROOT="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
: "${SDK_ROOT:?Set ANDROID_HOME to your Android SDK}"
BT="$SDK_ROOT/build-tools/35.0.0"
ANDROID_JAR="$SDK_ROOT/platforms/android-35/android.jar"
mkdir -p build/gen build/classes build/dex dist
python3 scripts/validate_story.py
"$BT/aapt2" compile --dir app/src/main/res -o build/resources.zip
"$BT/aapt2" link -o build/base.apk -I "$ANDROID_JAR" --manifest app/src/main/AndroidManifest.xml -A app/src/main/assets --java build/gen --auto-add-overlay -R build/resources.zip
find app/src/main/java build/gen -name '*.java' > build/sources.txt
javac -encoding UTF-8 -source 8 -target 8 -classpath "$ANDROID_JAR" -d build/classes @build/sources.txt
jar cf build/classes.jar -C build/classes .
"$BT/d8" --lib "$ANDROID_JAR" --min-api 26 --output build/dex build/classes.jar
python3 - <<'PY'
import zipfile, pathlib, shutil
shutil.copy('build/base.apk','build/unsigned.apk')
with zipfile.ZipFile('build/unsigned.apk','a',zipfile.ZIP_DEFLATED) as z:
    for p in pathlib.Path('build/dex').glob('*.dex'): z.write(p,p.name)
PY
"$BT/zipalign" -p -f 4 build/unsigned.apk build/aligned.apk
# Ephemeral development signing key. Never committed or uploaded.
keytool -genkeypair -keystore build/pilot.keystore -storepass android -keypass android -alias raining-pilot -keyalg RSA -keysize 2048 -validity 3650 -dname "CN=Raining Pilot, O=Raining, C=BR" >/dev/null 2>&1
"$BT/apksigner" sign --ks build/pilot.keystore --ks-key-alias raining-pilot --ks-pass pass:android --key-pass pass:android --out dist/Raining-v0.1.0.apk build/aligned.apk
"$BT/apksigner" verify --verbose dist/Raining-v0.1.0.apk
sha256sum dist/Raining-v0.1.0.apk > dist/SHA256SUMS.txt
