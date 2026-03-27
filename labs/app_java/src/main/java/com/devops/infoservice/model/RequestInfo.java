package com.devops.infoservice.model;

/**
 * Request information data model
 */
public class RequestInfo {
    private String clientIp;
    private String userAgent;
    private String method;
    private String path;

    public RequestInfo() {}

    public RequestInfo(String clientIp, String userAgent, String method, String path) {
        this.clientIp = clientIp;
        this.userAgent = userAgent;
        this.method = method;
        this.path = path;
    }

    // Getters and setters
    public String getClientIp() { return clientIp; }
    public void setClientIp(String clientIp) { this.clientIp = clientIp; }

    public String getUserAgent() { return userAgent; }
    public void setUserAgent(String userAgent) { this.userAgent = userAgent; }

    public String getMethod() { return method; }
    public void setMethod(String method) { this.method = method; }

    public String getPath() { return path; }
    public void setPath(String path) { this.path = path; }
}