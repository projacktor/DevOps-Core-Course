package com.devops.infoservice;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import com.devops.infoservice.service.InfoService;
import org.junit.jupiter.api.Test;

class InfoServiceTest {

  private final InfoService infoService = new InfoService();

  @Test
  void shouldReturnServiceInfo() {
    assertNotNull(infoService.getServiceInfo(), "Service info should not be null");
  }
}
