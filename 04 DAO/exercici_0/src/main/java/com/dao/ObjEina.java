package com.dao;

import java.util.ArrayList;

public class ObjEina {
    private int id;
    private String nom;
    private int any;
    private ArrayList<Integer> llenguatges;

    public ObjEina(int id, String nom, int any, ArrayList<Integer> llenguatges) {
        this.id = id;
        this.nom = nom;
        this.any = any;
        this.llenguatges = llenguatges;
    }

    public int getId() {
        return id;
    }

    public String getNom() {
        return nom;
    }

    public int getAny() {
        return any;
    }

    public ArrayList<Integer> getLlenguatges() {
        return llenguatges;
    }

    public void setAny(int any) {
        this.any = any;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setLlenguatges(ArrayList<Integer> llenguatges) {
        this.llenguatges = llenguatges;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    @Override
    public String toString() {
        return "Eina: " + id + " " + nom + ", " + any + " - " + llenguatges;
    }
}
