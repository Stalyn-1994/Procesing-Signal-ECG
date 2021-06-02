package com.example.ecgclient.modelo;

import java.lang.reflect.Array;
import java.util.List;

public class pacientes {
    private int ci;
    private String name;
    private String address;
    private List signal;
    private  String imagen;
    private  String clean;


    public int getCi() {
        return ci;
    }

    public void setCi(int ci) {
        this.ci = ci;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public List getSignal() {
        return signal;
    }

    public void setSignal(List signal) {
        this.signal = signal;
    }

    public String getImagen() {
        return imagen;
    }

    public void setImagen(String imagen) {
        this.imagen = imagen;
    }

    public String getClean() {
        return clean;
    }

    public void setClean(String clean) {
        this.clean = clean;
    }
}
