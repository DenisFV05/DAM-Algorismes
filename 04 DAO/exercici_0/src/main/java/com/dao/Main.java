package com.dao;

import java.util.ArrayList;


public class Main {
   public static String basePath = System.getProperty("user.dir") + "/data/";
   public static String llenguatgesPath = basePath + "llenguatges.json";
   public static String einesPath = basePath + "eines.json";
   public static String softwarePath = basePath + "software.json";


   public static void main(String[] args) {


       DaoEina         daoEina = new DaoEina();
       DaoLlenguatge   daoLlenguatge = new DaoLlenguatge();
       DaoSoftware     daoSoftware = new DaoSoftware();


       // Afegir una eina
       ArrayList<Integer> aLlenguatges0 = new ArrayList<>();
       aLlenguatges0.add(0);
       aLlenguatges0.add(1);
       ObjEina objEina0 = new ObjEina (5, "Text", 2000, aLlenguatges0);
       daoEina.add(objEina0);


       // Modificar una eina
       ArrayList<Integer> aLlenguatges1 = new ArrayList<>();
       aLlenguatges1.add(0);
       aLlenguatges1.add(1);
       aLlenguatges1.add(2);
       ObjEina objEina1 = new ObjEina (5, "TextEdit", 2001, aLlenguatges1);
       daoEina.update(5, objEina1);


       // Afegir llenguatge a eina
       daoEina.setLlenguatgesAdd(5, 3);


       // Treure llenguatge a eina
       daoEina.setLlenguatgesDelete(5, 2);


       // Llistar les eines
       daoEina.print();


       // Esborrar eina amb id 5
       daoEina.delete(5);


       // Afegir un llenguatge
       ObjLlenguatge objLlenguatge0 = new ObjLlenguatge(5, "Dart", 2011, "facil", 8);
       daoLlenguatge.add(objLlenguatge0);


       // Canviar el nom
       daoLlenguatge.setNom(5, "Dart+Flutter");


       // Canviar l'any
       daoLlenguatge.setAny(5, 2018);


       // Canvir dificultat
       daoLlenguatge.setDificultat(5, "mitja");


       // Canviar popularitat
       daoLlenguatge.setPopularitat(5, 9);


       // Llistar els llenguatges
       daoLlenguatge.print();


       // Esborrar llenguatge amb id 5
       daoLlenguatge.delete(5);


       // Afegir un software
       ArrayList<Integer> aLlenguatges2 = new ArrayList<>();
       aLlenguatges2.add(3);
       ObjSoftware objSoftware = new ObjSoftware(10, "webTool", 2022, aLlenguatges2);
       daoSoftware.add(objSoftware);


       // Llistar software
       daoSoftware.print();


       // Esborrar llenguatge amb id 5
       daoSoftware.delete(10);
   }
}