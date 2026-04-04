package com.devops.infoservice.model;

import java.util.List;

/**
 * Complete service response data model
 */
public class ServiceResponse {
    private ServiceInfo service;
    private SystemInfo system;
    private RuntimeInfo runtime;
    private RequestInfo request;
    private List<EndpointInfo> endpoints;

    public ServiceResponse() {}

    public ServiceResponse(ServiceInfo service, SystemInfo system, RuntimeInfo runtime, 
                          RequestInfo request, List<EndpointInfo> endpoints) {
        this.service = service;
        this.system = system;
        this.runtime = runtime;
        this.request = request;
        this.endpoints = endpoints;
    }

    // Getters and setters
    public ServiceInfo getService() { return service; }
    public void setService(ServiceInfo service) { this.service = service; }

    public SystemInfo getSystem() { return system; }
    public void setSystem(SystemInfo system) { this.system = system; }

    public RuntimeInfo getRuntime() { return runtime; }
    public void setRuntime(RuntimeInfo runtime) { this.runtime = runtime; }

    public RequestInfo getRequest() { return request; }
    public void setRequest(RequestInfo request) { this.request = request; }

    public List<EndpointInfo> getEndpoints() { return endpoints; }
    public void setEndpoints(List<EndpointInfo> endpoints) { this.endpoints = endpoints; }
}