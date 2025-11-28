package com.example.analysis;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point for the Property Analysis Service.
 *
 * This Spring Boot application exposes simple REST endpoints to return aggregate
 * statistics about the housing dataset.  The statistics are computed once at
 * startup for efficiency.
 */
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
