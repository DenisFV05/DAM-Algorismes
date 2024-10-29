package com.dao;

import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONObject;

public class DaoEina implements Dao<ObjEina> {

    // Método para escribir la lista de herramientas en un archivo JSON
    private void writeList(ArrayList<ObjEina> llista) {
        try {
            JSONArray jsonArray = new JSONArray();
            for (ObjEina eina : llista) {
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("id", eina.getId());
                jsonObject.put("nom", eina.getNom());
                jsonObject.put("any", eina.getAny());
                JSONArray jsonLlenguatges = new JSONArray(eina.getLlenguatges());
                jsonObject.put("llenguatges", jsonLlenguatges);
                jsonArray.put(jsonObject);
            }
            PrintWriter out = new PrintWriter(Main.einesPath);
            out.write(jsonArray.toString(4));
            out.flush();
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Método para obtener la posición de una herramienta en la lista según su ID
    private int getPosition(int id) {
        ArrayList<ObjEina> llista = getAll();
        for (int i = 0; i < llista.size(); i++) {
            if (llista.get(i).getId() == id) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public void add(ObjEina eina) {
        ArrayList<ObjEina> llista = getAll();
        if (get(eina.getId()) == null) {
            llista.add(eina);
            writeList(llista);
        }
    }

    @Override
    public ObjEina get(int id) {
        int pos = getPosition(id);
        return pos != -1 ? getAll().get(pos) : null;
    }

    @Override
    public ArrayList<ObjEina> getAll() {
        ArrayList<ObjEina> result = new ArrayList<>();
        try {
            String content = new String(Files.readAllBytes(Paths.get(Main.einesPath)));
            JSONArray jsonArray = new JSONArray(content);
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                int id = jsonObject.getInt("id");
                String nom = jsonObject.getString("nom");
                int any = jsonObject.getInt("any");
                JSONArray jsonLlenguatges = jsonObject.getJSONArray("llenguatges");
                ArrayList<Integer> llenguatges = new ArrayList<>();
                for (int j = 0; j < jsonLlenguatges.length(); j++) {
                    llenguatges.add(jsonLlenguatges.getInt(j));
                }
                result.add(new ObjEina(id, nom, any, llenguatges));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public void update(int id, ObjEina eina) {
        ArrayList<ObjEina> llista = getAll();
        int pos = getPosition(id);
        if (pos != -1) {
            llista.set(pos, eina);
            writeList(llista);
        }
    }

    @Override
    public void delete(int id) {
        ArrayList<ObjEina> llista = getAll();
        int pos = getPosition(id);
        if (pos != -1) {
            llista.remove(pos);
            writeList(llista);
        }
    }

    @Override
    public void print() {
        ArrayList<ObjEina> llista = getAll();
        llista.forEach(System.out::println);
    }

    // Métodos específicos para DaoEina
    public void setLlenguatgesAdd(int id, int idLlenguatge) {
        ObjEina eina = get(id);
        if (eina != null && !eina.getLlenguatges().contains(idLlenguatge)) {
            eina.getLlenguatges().add(idLlenguatge);
            update(id, eina);
        }
    }

    
    public void setLlenguatgesDelete(int id, int idLlenguatge) {
        ObjEina eina = get(id);
        if (eina != null) {
            eina.getLlenguatges().remove(Integer.valueOf(idLlenguatge));
            update(id, eina);
        }
    }

    @Override
    public void setAny(int id, int any) {
        ObjEina eina = get(id);
        if (eina != null) {
            eina.setAny(any);
            ArrayList<ObjEina> llista = getAll();
            int pos = getPosition(id);
            if (pos != -1) {
            eina.setAny(any);
            writeList(llista);
        }}
    }

    @Override
    public void setNom(int id, String nom) {
        ObjEina eina = get(id);
        if (eina != null) {
            eina.setNom(nom);;
            ArrayList<ObjEina> llista = getAll();
            int pos = getPosition(id);
            if (pos != -1) {
            eina.setNom(nom);;
            writeList(llista);
        }}
    }
}


