package com.devops.infoservice.model;

/**
 * Endpoint information data model
 */
public class EndpointInfo {
    private String path;
    private String method;
    private String description;

    public EndpointInfo() {}

    public EndpointInfo(String path, String method, String description) {
        this.path = path;
        this.method = method;
        this.description = description;
    }

    // Getters and setters
    public String getPath() { return path; }
    public void setPath(String path) { this.path = path; }

    public String getMethod() { return method; }
    public void setMethod(String method) { this.method = method; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}