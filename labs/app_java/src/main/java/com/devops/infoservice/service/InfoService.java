package com.devops.infoservice.service;

import com.devops.infoservice.model.*;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.time.Instant;
import java.time.ZoneId;
import java.util.Arrays;
import java.util.List;
import org.springframework.stereotype.Service;

/** Service for collecting system and service information */
@Service
public class InfoService {

  private final long startTime = System.currentTimeMillis();

  /** Get service information */
  public ServiceInfo getServiceInfo() {
    return new ServiceInfo(
        "devops-info-service", "1.0.0", "DevOps course info service", "Spring Boot");
  }

  /** Get system information */
  public SystemInfo getSystemInfo() {
    String hostname;
    try {
      hostname = InetAddress.getLocalHost().getHostName();
    } catch (UnknownHostException e) {
      hostname = "unknown";
    }

    return new SystemInfo(
        hostname,
        System.getProperty("os.name"),
        System.getProperty("os.version"),
        System.getProperty("os.arch"),
        Runtime.getRuntime().availableProcessors(),
        System.getProperty("java.version"));
  }

  /** Get runtime information */
  public RuntimeInfo getRuntimeInfo() {
    long uptime = getUptimeSeconds();
    return new RuntimeInfo(uptime, formatUptime(uptime), getCurrentTimeISO(), getTimezone());
  }

  /** Get request information */
  public RequestInfo getRequestInfo(String clientIp, String userAgent, String method, String path) {
    return new RequestInfo(clientIp, userAgent, method, path);
  }

  /** Get available endpoints */
  public List<EndpointInfo> getEndpoints() {
    return Arrays.asList(
        new EndpointInfo("/", "GET", "Service information"),
        new EndpointInfo("/health", "GET", "Health check"));
  }

  /** Get uptime in seconds */
  public long getUptimeSeconds() {
    return (System.currentTimeMillis() - startTime) / 1000;
  }

  /** Format uptime in human readable format */
  private String formatUptime(long seconds) {
    long hours = seconds / 3600;
    long minutes = (seconds % 3600) / 60;
    return String.format("%d hours, %d minutes", hours, minutes);
  }

  /** Get current time in ISO format */
  private String getCurrentTimeISO() {
    return Instant.now().toString();
  }

  /** Get system timezone */
  private String getTimezone() {
    return ZoneId.systemDefault().getId();
  }
}
