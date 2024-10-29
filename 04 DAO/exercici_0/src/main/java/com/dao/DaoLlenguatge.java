package com.dao;



import org.json.JSONArray;
import org.json.JSONObject;

import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

public class DaoLlenguatge implements Dao<ObjLlenguatge> {

    private void writeList(ArrayList<ObjLlenguatge> llista) {
        try {
            JSONArray jsonArray = new JSONArray();
            for (ObjLlenguatge llenguatge : llista) {
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("id", llenguatge.getId());
                jsonObject.put("nom", llenguatge.getNom());
                jsonObject.put("any", llenguatge.getAny());
                jsonObject.put("dificultat", llenguatge.getDificultat());
                jsonObject.put("popularitat", llenguatge.getPopularitat());
                jsonArray.put(jsonObject);
            }
            PrintWriter out = new PrintWriter(Main.llenguatgesPath);
            out.write(jsonArray.toString(4));
            out.flush();
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private int getPosition(int id) {
        ArrayList<ObjLlenguatge> llista = getAll();
        for (int i = 0; i < llista.size(); i++) {
            if (llista.get(i).getId() == id) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public void add(ObjLlenguatge llenguatge) {
        ArrayList<ObjLlenguatge> llista = getAll();
        if (get(llenguatge.getId()) == null) {
            llista.add(llenguatge);
            writeList(llista);
        }
    }

    @Override
    public ObjLlenguatge get(int id) {
        int pos = getPosition(id);
        return pos != -1 ? getAll().get(pos) : null;
    }

    @Override
    public ArrayList<ObjLlenguatge> getAll() {
        ArrayList<ObjLlenguatge> result = new ArrayList<>();
        try {
            String content = new String(Files.readAllBytes(Paths.get(Main.llenguatgesPath)));
            JSONArray jsonArray = new JSONArray(content);
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                int id = jsonObject.getInt("id");
                String nom = jsonObject.getString("nom");
                int any = jsonObject.getInt("any");
                String dificultat = jsonObject.getString("dificultat");
                int popularitat = jsonObject.getInt("popularitat");
                result.add(new ObjLlenguatge(id, nom, any, dificultat, popularitat));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public void update(int id, ObjLlenguatge llenguatge) {
        ArrayList<ObjLlenguatge> llista = getAll();
        int pos = getPosition(id);
        if (pos != -1) {
            llista.set(pos, llenguatge);
            writeList(llista);
        }
    }

    @Override
    public void delete(int id) {
        ArrayList<ObjLlenguatge> llista = getAll();
        int pos = getPosition(id);
        if (pos != -1) {
            llista.remove(pos);
            writeList(llista);
        }
    }

    @Override
    public void print() {
        ArrayList<ObjLlenguatge> llista = getAll();
        llista.forEach(System.out::println);
    }

    // Métodos específicos para DaoLlenguatge
    public void setNom(int id, String nom) {
        ObjLlenguatge llenguatge = get(id);
        if (llenguatge != null) {
            llenguatge.setNom(nom);
            update(id, llenguatge);
        }
    }

    public void setAny(int id, int any) {
        ObjLlenguatge llenguatge = get(id);
        if (llenguatge != null) {
            llenguatge.setAny(any);
            update(id, llenguatge);
        }
    }

    public void setDificultat(int id, String dificultat) {
        ObjLlenguatge llenguatge = get(id);
        if (llenguatge != null) {
            llenguatge.setDificultat(dificultat);
            update(id, llenguatge);
        }
    }

    public void setPopularitat(int id, int popularitat) {
        ObjLlenguatge llenguatge = get(id);
        if (llenguatge != null) {
            llenguatge.setPopularitat(popularitat);
            update(id, llenguatge);
        }
    }
}


