{ pkgs ? import <nixpkgs> {} }:

# Nix Docker image for python-info-service (Task 2 - Lab 18)
# Creates a fully reproducible Docker image without a base image

let
  # Import application from Task 1
  app = import ./default.nix { inherit pkgs; };
in
pkgs.dockerTools.buildLayeredImage {
  # Image name
  name = "python-info-service-nix";
  
  # Image tag
  tag = "1.0.0";
  
  # Critical for reproducibility: fixed timestamp
  # DO NOT use "now" - this breaks reproducibility
  created = "1970-01-01T00:00:01Z";
  
  # Image contents - only our app and necessary dependencies
  # Nix automatically includes all transitive dependencies (closure)
  contents = [ 
    app
    pkgs.coreutils
    pkgs.cacert
  ];
  
  # Docker image configuration
  config = {
    # Start command - use binary path from Nix store
    Cmd = [ "${app}/bin/python-info-service" ];
    
    # Exposed port (equivalent to EXPOSE in Dockerfile)
    ExposedPorts = {
      "8080/tcp" = {};
    };
    
    # User for running (equivalent to USER app in Dockerfile)
    User = "1000";  # UID for non-root user
    
    # Working directory (equivalent to WORKDIR in Dockerfile)
    WorkingDir = "/";
  };
}