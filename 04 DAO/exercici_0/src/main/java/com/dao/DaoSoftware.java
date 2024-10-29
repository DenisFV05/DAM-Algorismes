package com.dao;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

public class DaoSoftware implements Dao<ObjSoftware> {

    // Método para escribir la lista de software en un archivo JSON
    private void writeList(ArrayList<ObjSoftware> llista) {
        try {
            JSONArray jsonArray = new JSONArray();
            for (ObjSoftware software : llista) {
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("id", software.getId());
                jsonObject.put("nom", software.getNom());
                jsonObject.put("any", software.getAny());
                JSONArray jsonLlenguatges = new JSONArray(software.getLlenguatges());
                jsonObject.put("llenguatges", jsonLlenguatges);
                jsonArray.put(jsonObject);
            }
            PrintWriter out = new PrintWriter(Main.softwarePath);
            out.write(jsonArray.toString(4)); // 4 es el espaciado
            out.flush();
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Método para obtener la posición de un software en la lista según su ID
    private int getPosition(int id) {
        ArrayList<ObjSoftware> llista = getAll();
        for (int i = 0; i < llista.size(); i++) {
            if (llista.get(i).getId() == id) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public void add(ObjSoftware software) {
        ArrayList<ObjSoftware> llista = getAll();
        if (get(software.getId()) == null) {
            llista.add(software);
            writeList(llista);
        }
    }

    @Override
    public ObjSoftware get(int id) {
        int pos = getPosition(id);
        return pos != -1 ? getAll().get(pos) : null;
    }

    @Override
    public ArrayList<ObjSoftware> getAll() {
        ArrayList<ObjSoftware> result = new ArrayList<>();
        try {
            String content = new String(Files.readAllBytes(Paths.get(Main.softwarePath)));
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
                result.add(new ObjSoftware(id, nom, any, llenguatges));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public void update(int id, ObjSoftware software) {
        ArrayList<ObjSoftware> llista = getAll();
        int pos = getPosition(id);
        if (pos != -1) {
            llista.set(pos, software);
            writeList(llista);
        }
    }

    @Override
    public void delete(int id) {
        ArrayList<ObjSoftware> llista = getAll();
        int pos = getPosition(id);
        if (pos != -1) {
            llista.remove(pos);
            writeList(llista);
        }
    }

    @Override
    public void print() {
        ArrayList<ObjSoftware> llista = getAll();
        llista.forEach(System.out::println);
    }

    // Métodos específicos para DaoSoftware
    public void setLlenguatgesAdd(int id, int idLlenguatge) {
        ObjSoftware software = get(id);
        if (software != null && !software.getLlenguatges().contains(idLlenguatge)) {
            software.getLlenguatges().add(idLlenguatge);
            update(id, software);
        }
    }

    public void setLlenguatgesDelete(int id, int idLlenguatge) {
        ObjSoftware software = get(id);
        if (software != null) {
            software.getLlenguatges().remove(Integer.valueOf(idLlenguatge));
            update(id, software);
        }
    }
}

