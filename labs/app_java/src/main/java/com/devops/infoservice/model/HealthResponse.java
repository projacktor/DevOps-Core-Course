package com.devops.infoservice.model;

/** Health check response data model */
public class HealthResponse {
  private String status;
  private String timestamp;
  private long uptimeSeconds;

  public HealthResponse() {}

  public HealthResponse(String status, String timestamp, long uptimeSeconds) {
    this.status = status;
    this.timestamp = timestamp;
    this.uptimeSeconds = uptimeSeconds;
  }

  // Getters and setters
  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  public String getTimestamp() {
    return timestamp;
  }

  public void setTimestamp(String timestamp) {
    this.timestamp = timestamp;
  }

  public long getUptimeSeconds() {
    return uptimeSeconds;
  }

  public void setUptimeSeconds(long uptimeSeconds) {
    this.uptimeSeconds = uptimeSeconds;
  }
}
