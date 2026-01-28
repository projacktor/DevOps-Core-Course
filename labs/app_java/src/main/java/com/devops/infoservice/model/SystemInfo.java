package com.devops.infoservice.model;

/**
 * System information data model
 */
public class SystemInfo {
    private String hostname;
    private String platform;
    private String platformVersion;
    private String architecture;
    private int cpuCount;
    private String javaVersion;

    public SystemInfo() {}

    public SystemInfo(String hostname, String platform, String platformVersion, 
                     String architecture, int cpuCount, String javaVersion) {
        this.hostname = hostname;
        this.platform = platform;
        this.platformVersion = platformVersion;
        this.architecture = architecture;
        this.cpuCount = cpuCount;
        this.javaVersion = javaVersion;
    }

    // Getters and setters
    public String getHostname() { return hostname; }
    public void setHostname(String hostname) { this.hostname = hostname; }

    public String getPlatform() { return platform; }
    public void setPlatform(String platform) { this.platform = platform; }

    public String getPlatformVersion() { return platformVersion; }
    public void setPlatformVersion(String platformVersion) { this.platformVersion = platformVersion; }

    public String getArchitecture() { return architecture; }
    public void setArchitecture(String architecture) { this.architecture = architecture; }

    public int getCpuCount() { return cpuCount; }
    public void setCpuCount(int cpuCount) { this.cpuCount = cpuCount; }

    public String getJavaVersion() { return javaVersion; }
    public void setJavaVersion(String javaVersion) { this.javaVersion = javaVersion; }
}