package com.example.analysis.controller;

import com.example.analysis.model.PropertyStats;
import com.example.analysis.service.MarketService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * REST controller exposing market analysis endpoints.
 */
@RestController
public class MarketController {
    private final MarketService marketService;

    public MarketController(MarketService marketService) {
        this.marketService = marketService;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "ok");
    }

    @GetMapping("/statistics")
    public PropertyStats statistics() {
        return marketService.getStats();
    }
}
