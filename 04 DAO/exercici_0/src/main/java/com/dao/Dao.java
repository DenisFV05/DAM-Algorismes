package com.dao;

import java.util.ArrayList;

public interface Dao<T> {

    void add(T t); // Equival a Create

    T get(int id); // Equival a Read
    ArrayList<T> getAll();

    void update(int id, T t);

    void delete(int id); 
    
    void print();
}
