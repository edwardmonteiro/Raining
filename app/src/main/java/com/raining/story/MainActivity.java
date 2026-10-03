package com.raining.story;

import android.app.*;
import android.content.*;
import android.graphics.*;
import android.graphics.drawable.*;
import android.net.Uri;
import android.os.*;
import android.view.*;
import android.widget.*;
import org.json.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.zip.*;

/** Native, offline illustrated story reader. Packs are data, never executable code. */
public class MainActivity extends Activity {
    final int BG=Color.rgb(17,27,33), PAPER=Color.rgb(248,238,224), GOLD=Color.rgb(232,190,141), MUTED=Color.rgb(169,185,187), PANEL=Color.rgb(28,43,50);
    LinearLayout root;
    JSONObject episode;
    Map<String,JSONObject> cards=new HashMap<>();
    ArrayList<String> history=new ArrayList<>();
    JSONObject choices=new JSONObject();
    android.content.SharedPreferences prefs;
    File packDir;
    String current, page="home";
    boolean finished=false, loading=false;
    int fontSize=21;
    final LinkedHashMap<String,Bitmap> bitmaps=new LinkedHashMap<>();

    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        prefs=getSharedPreferences("raining",MODE_PRIVATE);
        fontSize=prefs.getInt("font",21);
        getWindow().setStatusBarColor(BG); getWindow().setNavigationBarColor(BG);
        try {
            String selected=prefs.getString("selected","");
            File saved=new File(getFilesDir(),"packs/"+selected);
            if(!selected.isEmpty()&&new File(saved,"episode.json").exists()) loadEpisode(saved); else loadEpisode(null);
            home();
        } catch(Exception ex){ new AlertDialog.Builder(this).setTitle("Não foi possível abrir o episódio").setMessage(ex.getMessage()).setPositiveButton("Fechar",(d,w)->finish()).show(); }
    }
    int dp(float n){return (int)(n*getResources().getDisplayMetrics().density+.5f);}
    LinearLayout column(){LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);return l;}
    LinearLayout row(){LinearLayout l=new LinearLayout(this);l.setGravity(Gravity.CENTER_VERTICAL);return l;}
    GradientDrawable shape(int color,int radius){GradientDrawable d=new GradientDrawable();d.setColor(color);d.setCornerRadius(dp(radius));return d;}
    void gap(LinearLayout l,int h){View v=new View(this);l.addView(v,new LinearLayout.LayoutParams(1,dp(h)));}
    TextView text(String s,int size,int color){TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(color);t.setIncludeFontPadding(false);t.setLineSpacing(dp(3),1f);return t;}
    TextView label(String s){TextView t=text(s,11,GOLD);t.setLetterSpacing(.14f);t.setTypeface(Typeface.DEFAULT,Typeface.BOLD);return t;}
    TextView title(String s,int size){TextView t=text(s,size,PAPER);t.setTypeface(Typeface.create("serif",Typeface.NORMAL));return t;}
    Button button(String s,boolean primary,Runnable action){
        Button b=new Button(this);b.setText(s);b.setAllCaps(false);b.setTextSize(15);b.setTextColor(primary?BG:PAPER);b.setMinHeight(dp(52));b.setMinimumHeight(dp(52));b.setPadding(dp(16),dp(12),dp(16),dp(12));
        GradientDrawable gd=shape(primary?GOLD:PANEL,14);if(!primary)gd.setStroke(dp(1),Color.rgb(60,78,83));
        b.setBackground(new RippleDrawable(android.content.res.ColorStateList.valueOf(0x22808080),gd,null));
        b.setOnClickListener(v->action.run());return b;
    }
    void fullButton(LinearLayout l,String s,boolean primary,Runnable run){l.addView(button(s,primary,run),new LinearLayout.LayoutParams(-1,-2));gap(l,10);}
    void shell(String mode){
        page=mode;root=column();root.setBackgroundColor(BG);
        if(Build.VERSION.SDK_INT>=30){getWindow().setDecorFitsSystemWindows(false);
            root.setOnApplyWindowInsetsListener((v,insets)->{android.graphics.Insets x=insets.getInsets(WindowInsets.Type.systemBars()|WindowInsets.Type.displayCutout());v.setPadding(x.left,x.top,x.right,x.bottom);return insets;});
        } else root.setFitsSystemWindows(true);
        setContentView(root);
    }
    void header(String center,Runnable back){
        LinearLayout r=row();r.setPadding(dp(14),dp(2),dp(14),dp(2));
        Button left=button("‹",false,back);left.setTextSize(28);left.setPadding(0,0,0,0);left.setContentDescription("Voltar");r.addView(left,new LinearLayout.LayoutParams(dp(48),dp(48)));
        TextView t=label(center);t.setGravity(Gravity.CENTER);r.addView(t,new LinearLayout.LayoutParams(0,dp(48),1));
        Button settings=button("Aa",false,()->settings());settings.setPadding(0,0,0,0);settings.setContentDescription("Tamanho do texto");r.addView(settings,new LinearLayout.LayoutParams(dp(48),dp(48)));root.addView(r,new LinearLayout.LayoutParams(-1,dp(56)));
    }
    ScrollView scroll(LinearLayout parent){ScrollView s=new ScrollView(this);s.setFillViewport(false);s.setVerticalScrollBarEnabled(false);parent.addView(s,new LinearLayout.LayoutParams(-1,0,1));return s;}
    InputStream asset(String name)throws IOException{return packDir==null?getAssets().open(name):new FileInputStream(new File(packDir,name));}
    String read(InputStream in,int max)throws IOException{try(InputStream x=in;ByteArrayOutputStream out=new ByteArrayOutputStream()){byte[] b=new byte[8192];int n;while((n=x.read(b))!=-1){if(out.size()+n>max)throw new IOException("Arquivo grande demais");out.write(b,0,n);}return new String(out.toByteArray(),StandardCharsets.UTF_8);}}
    ImageView image(String path,String alt,int h){ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setContentDescription(alt);im.setBackground(shape(PANEL,18));im.setClipToOutline(true);
        try{Bitmap bm=bitmaps.get(path);if(bm==null){try(InputStream in=asset(path)){bm=BitmapFactory.decodeStream(in);}if(bm==null)throw new IOException("Imagem inválida");bitmaps.put(path,bm);if(bitmaps.size()>5)bitmaps.remove(bitmaps.keySet().iterator().next());}im.setImageBitmap(bm);}catch(Exception e){im.setContentDescription("Ilustração indisponível");}
        im.setLayoutParams(new LinearLayout.LayoutParams(-1,dp(h)));return im;
    }
    String prefix(){return episode.optString("id")+".";}
    void loadEpisode(File dir)throws Exception{
        packDir=dir;episode=new JSONObject(read(asset("episode.json"),200000));validate(episode);
        cards.clear();JSONArray all=episode.getJSONArray("cards");for(int i=0;i<all.length();i++){JSONObject c=all.getJSONObject(i);cards.put(c.getString("id"),c);}
        bitmaps.clear();current=prefs.getString(prefix()+"current",episode.getString("start"));if(!cards.containsKey(current))current=episode.getString("start");
        history.clear();JSONArray saved=new JSONArray(prefs.getString(prefix()+"history","[]"));for(int i=0;i<saved.length();i++)if(cards.containsKey(saved.getString(i)))history.add(saved.getString(i));
        choices=new JSONObject(prefs.getString(prefix()+"choices","{}"));finished=prefs.getBoolean(prefix()+"finished",false);
        prefs.edit().putString("selected",dir==null?"":dir.getName()).apply();
    }
    void save(){prefs.edit().putString(prefix()+"current",current).putString(prefix()+"history",new JSONArray(history).toString()).putString(prefix()+"choices",choices.toString()).putBoolean(prefix()+"finished",finished).apply();}
    void home(){
        shell("home");LinearLayout bar=row();bar.setPadding(dp(24),dp(16),dp(24),dp(12));TextView brand=label("R A I N I N G");bar.addView(brand,new LinearLayout.LayoutParams(0,-2,1));TextView off=text("OFFLINE  ·  01",10,MUTED);bar.addView(off);root.addView(bar);
        ScrollView s=scroll(root);LinearLayout body=column();body.setPadding(dp(22),0,dp(22),dp(16));s.addView(body);
        int height=Math.max(260,Math.min(430,(int)(getResources().getDisplayMetrics().heightPixels/getResources().getDisplayMetrics().density*.46)));
        FrameLayout hero=new FrameLayout(this);hero.setBackground(shape(PANEL,20));hero.setClipToOutline(true);ImageView art=image(episode.optString("cover"),"Hana chega ao restaurante sob a chuva",height);hero.addView(art,new FrameLayout.LayoutParams(-1,-1));
        View shade=new View(this);shade.setBackground(new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x00000000,0x00111B21,0xF2111B21}));hero.addView(shade,new FrameLayout.LayoutParams(-1,-1));
        LinearLayout words=column();words.setPadding(dp(22),dp(16),dp(20),dp(24));words.addView(label("UM DORAMA PARA LER E SENTIR"));gap(words,12);words.addView(title("Quando a\nchuva passar",34));FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-2,Gravity.BOTTOM);hero.addView(words,wp);body.addView(hero,new LinearLayout.LayoutParams(-1,dp(height)));
        gap(body,22);body.addView(label("EPISÓDIO "+String.format(java.util.Locale.ROOT,"%02d",episode.optInt("episode",1))+"   /   CERCA DE 3 MIN"));gap(body,9);body.addView(title(episode.optString("title"),27));gap(body,8);body.addView(text(episode.optString("subtitle"),15,MUTED));gap(body,20);
        String action=finished?"Revisitar episódio  ↗":history.isEmpty()?"Começar a história  →":"Continuar · card "+cards.get(current).optInt("step")+"  →";
        fullButton(body,action,true,()->{if(finished)restartPrompt();else reader();});
        LinearLayout secondary=row();Button album=button("Lembranças",false,()->album());Button packs=button("Episódios",false,()->episodes());LinearLayout.LayoutParams half=new LinearLayout.LayoutParams(0,-2,1);half.setMargins(0,0,dp(8),0);secondary.addView(album,half);secondary.addView(packs,new LinearLayout.LayoutParams(0,-2,1));body.addView(secondary);gap(body,15);
        TextView note=text("Leia no seu ritmo. Suas escolhas ficam guardadas.",12,MUTED);note.setGravity(Gravity.CENTER);body.addView(note);
    }
    void reader(){
        shell("reader");JSONObject c=cards.get(current);header(episode.optString("title").toUpperCase(java.util.Locale.ROOT),()->home());
        LinearLayout dots=row();dots.setPadding(dp(24),dp(5),dp(24),dp(9));int step=c.optInt("step",1),total=episode.optInt("cardCount",18);for(int i=1;i<=total;i++){View dot=new View(this);dot.setBackground(shape(i<=step?GOLD:0xff33454d,2));LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(0,dp(3),1);p.setMargins(dp(1),0,dp(1),0);dots.addView(dot,p);}dots.setContentDescription("Card "+step+" de "+total);root.addView(dots);
        ScrollView s=scroll(root);LinearLayout body=column();body.setPadding(dp(20),dp(3),dp(20),dp(8));s.addView(body);
        int h=Math.max(210,Math.min(440,(int)(getResources().getDisplayMetrics().heightPixels/getResources().getDisplayMetrics().density*.43)));
        body.addView(image(c.optString("image"),description(c.optString("image")),h));gap(body,17);
        LinearLayout meta=row();meta.addView(label(c.optString("speaker")),new LinearLayout.LayoutParams(0,-2,1));meta.addView(text(String.format(java.util.Locale.ROOT,"%02d / %02d",step,total),11,MUTED));body.addView(meta);gap(body,10);
        TextView prose=text(c.optString("text"),fontSize,PAPER);prose.setLineSpacing(dp(5),1f);body.addView(prose);gap(body,14);
        if(c.has("caption")){TextView caption=text(c.optString("caption"),13,MUTED);caption.setTypeface(Typeface.create("serif",Typeface.ITALIC));body.addView(caption);gap(body,14);}
        JSONArray opts=c.optJSONArray("choices");if(opts!=null){for(int i=0;i<opts.length();i++){JSONObject o=opts.optJSONObject(i);fullButton(body,o.optString("label"),false,()->choose(o));}}
        LinearLayout footer=row();footer.setPadding(dp(20),dp(8),dp(20),dp(8));Button prev=button("‹",false,()->previous());prev.setContentDescription("Card anterior");prev.setEnabled(!history.isEmpty());prev.setAlpha(history.isEmpty()?.35f:1f);footer.addView(prev,new LinearLayout.LayoutParams(dp(52),dp(52)));
        Button next=button(c.optBoolean("ending")?"Guardar este capítulo  ✓":opts!=null?"Escolha uma resposta acima":"Próximo card  →",opts==null,()->{if(c.optBoolean("ending")){finished=true;save();ending();}else if(c.has("next"))advance(c.optString("next"));});
        next.setEnabled(opts==null);if(opts!=null)next.setAlpha(.55f);LinearLayout.LayoutParams np=new LinearLayout.LayoutParams(0,-2,1);np.setMargins(dp(10),0,0,0);footer.addView(next,np);root.addView(footer);
    }
    String description(String path){if(path.contains("jiho"))return "Jiho, um antigo amigo, com uma sacola de compras na porta";if(path.contains("hana"))return "Hana segura uma tigela de sopa, emocionada";if(path.contains("letter"))return "Um envelope e uma fotografia antiga sob uma tigela";if(path.contains("table"))return "Duas tigelas na mesa de um restaurante acolhedor";return "Hana volta ao restaurante numa noite de chuva";}
    void advance(String id){if(!cards.containsKey(id))return;history.add(current);current=id;save();reader();}
    void choose(JSONObject option){try{choices.put(current,option);advance(option.getString("next"));}catch(Exception e){toast("Não foi possível registrar a escolha.");}}
    void previous(){if(history.isEmpty())return;current=history.remove(history.size()-1);choices.remove(current);finished=false;save();reader();}
    void restartPrompt(){new AlertDialog.Builder(this).setTitle("Recomeçar este episódio?").setMessage("As escolhas deste episódio serão substituídas pela nova leitura.").setNegativeButton("Cancelar",null).setPositiveButton("Recomeçar",(d,w)->{history.clear();choices=new JSONObject();finished=false;current=episode.optString("start");save();reader();}).show();}
    void ending(){
        shell("ending");header("CAPÍTULO GUARDADO",()->home());ScrollView s=scroll(root);LinearLayout b=column();b.setPadding(dp(24),dp(20),dp(24),dp(24));s.addView(b);
        b.addView(image(episode.optString("cover"),"Lembrança do episódio",230));gap(b,22);b.addView(label("FIM DO EPISÓDIO "+episode.optInt("episode",1)));gap(b,12);b.addView(title(episode.optString("endingTitle","Hoje, você ficou\npara jantar."),32));gap(b,14);
        b.addView(text("Algumas respostas podem esperar. A sua versão deste encontro ficou guardada.",18,PAPER));gap(b,24);memories(b);gap(b,18);
        b.addView(label("A HISTÓRIA CONTINUA"));gap(b,8);b.addView(title(episode.optString("nextTitle","Um novo capítulo"),24));gap(b,8);b.addView(text("Próximo episódio ainda não publicado.",14,MUTED));gap(b,22);fullButton(b,"Voltar ao início",true,()->home());fullButton(b,"Ler com outras escolhas",false,()->restartPrompt());
    }
    void memories(LinearLayout b){int count=0;JSONArray list=episode.optJSONArray("cards");for(int i=0;i<list.length();i++){JSONObject choice=choices.optJSONObject(list.optJSONObject(i).optString("id"));if(choice!=null){LinearLayout tile=column();tile.setPadding(dp(16),dp(15),dp(16),dp(15));tile.setBackground(shape(PANEL,14));tile.addView(label("LEMBRANÇA 0"+(++count)));gap(tile,9);tile.addView(text(choice.optString("memory"),17,PAPER));b.addView(tile);gap(b,12);}}
        if(count==0){b.addView(text("Suas lembranças aparecem aqui depois das primeiras escolhas.",18,MUTED));}
    }
    void album(){shell("album");header("SUAS LEMBRANÇAS",()->home());ScrollView s=scroll(root);LinearLayout b=column();b.setPadding(dp(24),dp(24),dp(24),dp(24));s.addView(b);b.addView(title("O que ficou\ncom você",34));gap(b,12);b.addView(text(episode.optString("title"),15,MUTED));gap(b,26);memories(b);gap(b,18);fullButton(b,"Voltar à história",true,()->{if(finished)ending();else reader();});}
    void settings(){new AlertDialog.Builder(this).setTitle("Tamanho da leitura").setSingleChoiceItems(new String[]{"Confortável","Grande","Extra grande"},fontSize==21?0:fontSize==25?1:2,(d,w)->{fontSize=new int[]{21,25,29}[w];prefs.edit().putInt("font",fontSize).apply();d.dismiss();refresh();}).setNegativeButton("Fechar",null).show();}
    void refresh(){switch(page){case "reader":reader();break;case "album":album();break;case "ending":ending();break;case "episodes":episodes();break;default:home();}}
    void episodes(){
        shell("episodes");header("EPISÓDIOS",()->home());ScrollView s=scroll(root);LinearLayout b=column();b.setPadding(dp(24),dp(24),dp(24),dp(24));s.addView(b);b.addView(title("Histórias para\nlevar com você",32));gap(b,20);
        fullButton(b,"01 · Uma mesa para dois",packDir==null,()->select(null));
        File dir=new File(getFilesDir(),"packs");File[] dirs=dir.listFiles();if(dirs!=null)for(File file:dirs){if(!file.isDirectory()||file.getName().startsWith("."))continue;try{JSONObject e=new JSONObject(read(new FileInputStream(new File(file,"episode.json")),200000));fullButton(b,String.format(java.util.Locale.ROOT,"%02d",e.optInt("episode"))+" · "+e.optString("title"),file.equals(packDir),()->select(file));}catch(Exception ignored){}}
        gap(b,12);b.addView(text("Novos episódios chegam em packs. Importe um arquivo .raining ou .zip para ler offline.",16,MUTED));gap(b,18);fullButton(b,"Importar pack de episódio",false,()->{Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("*/*");i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,40);});
        gap(b,18);b.addView(label("SOBRE ESTE PILOTO"));gap(b,10);b.addView(text("Raining 0.1.0\nHistória original em português. Ilustrações originais geradas com IA. Sem anúncios, conta ou coleta de dados.\n\nTema: luto e reencontro. Leitura no seu ritmo.\n\nOs packs deste piloto são importados manualmente. Download automático e dublagem ficam para versões futuras.",14,MUTED));
    }
    void select(File dir){try{save();loadEpisode(dir);home();}catch(Exception e){toast("Não foi possível abrir o pack.");}}
    @Override protected void onActivityResult(int req,int code,Intent data){super.onActivityResult(req,code,data);if(req==40&&code==RESULT_OK&&data!=null&&data.getData()!=null){loading=true;ProgressDialog progress=ProgressDialog.show(this,"Importando episódio","Verificando imagens e história…",true,false);Uri uri=data.getData();new Thread(()->{try{File dir=importPack(uri);runOnUiThread(()->{loading=false;progress.dismiss();select(dir);toast("Episódio adicionado.");});}catch(Exception e){runOnUiThread(()->{loading=false;progress.dismiss();new AlertDialog.Builder(this).setTitle("Pack não importado").setMessage(e.getMessage()).setPositiveButton("Entendi",null).show();});}}).start();}}
    File importPack(Uri uri)throws Exception{
        File parent=new File(getFilesDir(),"packs");parent.mkdirs();File temp=new File(parent,".incoming-"+System.nanoTime());temp.mkdirs();
        try{
            long total=0;int count=0;Set<String> names=new HashSet<>();
            try(InputStream src=getContentResolver().openInputStream(uri);ZipInputStream zip=new ZipInputStream(src)){
                ZipEntry z;byte[] buf=new byte[8192];while((z=zip.getNextEntry())!=null){if(z.isDirectory())continue;String name=z.getName();if(++count>150||!name.matches("[a-zA-Z0-9_./-]+")||name.startsWith("/")||name.contains("..")||!names.add(name))throw new IOException("Estrutura de pack inválida.");
                    if(!name.equals("episode.json")&&!name.matches("art/[a-zA-Z0-9_-]+\\.(jpg|png|webp)"))throw new IOException("O pack contém arquivos não permitidos.");
                    File dst=new File(temp,name);dst.getParentFile().mkdirs();long size=0;try(OutputStream out=new FileOutputStream(dst)){int n;while((n=zip.read(buf))!=-1){size+=n;total+=n;if(size>8_000_000||total>40_000_000)throw new IOException("O pack ultrapassa o limite de 40 MB.");out.write(buf,0,n);}}
                }
            }
            JSONObject e=new JSONObject(read(new FileInputStream(new File(temp,"episode.json")),200000));validate(e);
            Set<String> images=new HashSet<>();images.add(e.getString("cover"));JSONArray cs=e.getJSONArray("cards");for(int i=0;i<cs.length();i++)images.add(cs.getJSONObject(i).getString("image"));
            for(String name:images){if(!name.matches("art/[a-zA-Z0-9_-]+\\.(jpg|png|webp)"))throw new IOException("Caminho de imagem inválido.");File im=new File(temp,name);BitmapFactory.Options o=new BitmapFactory.Options();o.inJustDecodeBounds=true;BitmapFactory.decodeFile(im.getPath(),o);if(o.outWidth<1||o.outHeight<1||o.outWidth>2400||o.outHeight>2400)throw new IOException("Imagem ausente, inválida ou maior que 2400 pixels.");}
            String id=e.getString("id");if(id.equals("uma-mesa-para-dois"))throw new IOException("O primeiro episódio já está instalado.");File target=new File(parent,id);if(target.exists())throw new IOException("Este episódio já está instalado. O progresso foi preservado.");if(!temp.renameTo(target))throw new IOException("Não foi possível guardar o episódio.");return target;
        }finally{removeTree(temp);}
    }
    void removeTree(File f){File[] c=f.listFiles();if(c!=null)for(File x:c)removeTree(x);f.delete();}
    static void validate(JSONObject e)throws Exception{
        if(e.optInt("schemaVersion")!=1||!e.optString("id").matches("[a-z0-9-]{1,60}"))throw new IOException("Versão ou identificação de pack incompatível.");
        if(e.optString("title").isEmpty()||e.optString("title").length()>100||e.optInt("cardCount")<1||e.optInt("cardCount")>100)throw new IOException("Metadados inválidos.");
        JSONArray cs=e.getJSONArray("cards");if(cs.length()<1||cs.length()>150)throw new IOException("Quantidade de cards inválida.");Map<String,JSONObject> map=new HashMap<>();
        for(int i=0;i<cs.length();i++){JSONObject c=cs.getJSONObject(i);String id=c.getString("id");if(!id.matches("[a-z0-9-]{1,60}")||map.put(id,c)!=null||c.getString("text").length()>1500||c.optInt("step")<1||c.optInt("step")>e.optInt("cardCount"))throw new IOException("Card inválido.");if(!c.getString("image").matches("art/[a-zA-Z0-9_-]+\\.(jpg|png|webp)"))throw new IOException("Imagem inválida.");}
        if(!map.containsKey(e.getString("start")))throw new IOException("Início do episódio ausente.");
        for(JSONObject c:map.values()){
            int modes=(c.has("choices")?1:0)+(c.has("next")?1:0)+(c.optBoolean("ending")?1:0);if(modes!=1)throw new IOException("Card sem continuação válida.");
            if(c.has("next")&&!map.containsKey(c.getString("next")))throw new IOException("Continuação ausente.");
            JSONArray os=c.optJSONArray("choices");if(os!=null){if(os.length()<2||os.length()>4)throw new IOException("Escolhas inválidas.");for(int i=0;i<os.length();i++){JSONObject o=os.getJSONObject(i);if(!map.containsKey(o.getString("next"))||o.getString("label").isEmpty()||o.getString("label").length()>100||o.getString("memory").length()>300)throw new IOException("Escolha inválida.");}}
        }
        walk(e.getString("start"),map,new HashSet<>(),new HashSet<>());
    }
    static void walk(String id,Map<String,JSONObject> map,Set<String> active,Set<String> done)throws Exception{if(done.contains(id))return;if(!active.add(id))throw new IOException("O episódio contém um ciclo.");JSONObject c=map.get(id);if(c.has("next"))walk(c.getString("next"),map,active,done);JSONArray os=c.optJSONArray("choices");if(os!=null)for(int i=0;i<os.length();i++)walk(os.getJSONObject(i).getString("next"),map,active,done);active.remove(id);done.add(id);}
    void toast(String s){Toast.makeText(this,s,Toast.LENGTH_LONG).show();}
    @Override public void onBackPressed(){if(loading)return;if(!page.equals("home"))home();else super.onBackPressed();}
    @Override protected void onPause(){super.onPause();if(episode!=null)save();}
}
