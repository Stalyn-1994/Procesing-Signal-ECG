package com.example.ecgclient;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;
import com.example.ecgclient.inter.JsonPlaceHolderApi;
import com.example.ecgclient.modelo.pacientes;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {
    private TextView sal;
    private ImageView imagen;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        sal=findViewById(R.id.salida);
        imagen=findViewById(R.id.subir);
        getData();
        



    }
    public void getData(){


        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(" https://optativaproyecto.herokuapp.com/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        JsonPlaceHolderApi jsonPlaceHolderApi = retrofit.create(JsonPlaceHolderApi.class);
        Call<List<pacientes>> call = jsonPlaceHolderApi.getPacientes();
        call.enqueue(new Callback<List<pacientes>>() {
                         @Override
                         public void onResponse(Call<List<pacientes>> call, Response<List<pacientes>> response) {
                             if(!response.isSuccessful()){
                                sal.setText("Codigo: "+response.code());
                                 return;
                             }

                             List<pacientes> postsList = response.body();

                             for(pacientes post: postsList){
                                 String content = "";
                                 content += "ci:"+ post.getCi()+ "\n";
                                 content += "name:"+ post.getName() + "\n";
                                 content += "address:"+ post.getAddress() + "\n";

                                 sal.append(content);

                             }
                         }

                         @Override
                         public void onFailure(Call<List<pacientes>> call, Throwable t) {
                             sal.setText(t.getMessage());
                         }
                     } );


        /*
        String services="http://localhost:5000/listar";
        StrictMode.ThreadPolicy policy=new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        URL url=null;
        HttpURLConnection conn;
        try {
            url=new URL(services);
            conn=(HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();
            BufferedReader in =new BufferedReader(new InputStreamReader((conn.getInputStream())));
            String inputLine;
            StringBuffer response=new StringBuffer();
            String json="";
            while ((inputLine=in.readLine())!=null){
                response.append(inputLine);
            }
            json=response.toString();
            JSONArray jsonArr=null;
            jsonArr=new JSONArray(json);
            String mensaje="";
             for(int i=0;i<jsonArr.length();i++){
                 JSONObject jsonObject=jsonArr.getJSONObject(i);
                 Log.d("SLIDA",jsonObject.optString("ci"));
                 mensaje+="DESCRIPTION"+i+" "+jsonObject.optString("ci")+"\n";
             }
             sal.setText(mensaje);

        }catch (MalformedURLException e){
            e.printStackTrace();

        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {            e.printStackTrace();
        }

         */


    }
}