package com.example.ecgclient.inter;
import com.example.ecgclient.modelo.pacientes;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;

public interface JsonPlaceHolderApi {
    @GET("listar")
    Call<List<pacientes>> getPacientes();
}
