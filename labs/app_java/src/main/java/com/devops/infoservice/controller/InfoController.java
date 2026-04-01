package com.devops.infoservice.controller;

import com.devops.infoservice.model.*;
import com.devops.infoservice.service.InfoService;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Main REST controller for DevOps Info Service */
@RestController
public class InfoController {

  private static final Logger LOGGER = LoggerFactory.getLogger(InfoController.class);

  @Autowired private InfoService infoService;

  /** Main endpoint - service and system information */
  @GetMapping("/")
  public ServiceResponse getInfo(HttpServletRequest request) {
    String clientIp = getClientIpAddress(request);
    String userAgent = request.getHeader("User-Agent");

    LOGGER.info(
        "endpoint=root method={} path={} client={} user_agent={} uptime_seconds={}",
        request.getMethod(),
        request.getRequestURI(),
        clientIp,
        userAgent,
        infoService.getUptimeSeconds());

    return new ServiceResponse(
        infoService.getServiceInfo(),
        infoService.getSystemInfo(),
        infoService.getRuntimeInfo(),
        infoService.getRequestInfo(
            clientIp, userAgent, request.getMethod(), request.getRequestURI()),
        infoService.getEndpoints());
  }

  /** Health check endpoint */
  @GetMapping("/health")
  public HealthResponse health() {
    long uptime = infoService.getUptimeSeconds();
    String timestamp = java.time.Instant.now().toString();

    LOGGER.info("endpoint=health status=healthy uptime_seconds={} timestamp={}", uptime, timestamp);

    return new HealthResponse("healthy", timestamp, uptime);
  }

  /** Extract client IP address from request */
  private String getClientIpAddress(HttpServletRequest request) {
    String xForwardedFor = request.getHeader("X-Forwarded-For");
    if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
      return xForwardedFor.split(",")[0].trim();
    }

    String xRealIp = request.getHeader("X-Real-IP");
    if (xRealIp != null && !xRealIp.isEmpty()) {
      return xRealIp;
    }

    return request.getRemoteAddr();
  }
}
