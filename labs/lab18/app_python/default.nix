{ pkgs ? import <nixpkgs> {} }:

# Nix derivation  for python-info-service lab1
# This derivation allows bit-for-bit replicable build
pkgs.python3Packages.buildPythonApplication {
  # pkg name
  pname = "python-info-service";
  
  # pkg version
  version = "1.0.0";
  
  # The source is current dir
  src = ./.;
  
  # "other" format used for app whithout specification setup.py/pyproject.toml
  format = "other";
  
  # we declare only main Python dependencies
  # while Nix will automatically resolve all transitionals
  propagatedBuildInputs = with pkgs.python3Packages; [
    # basic deps from requirements.txt
    fastapi
    uvicorn
    prometheus-client
    python-json-logger
    
    # secondary utils
    pydantic
    httpx
    python-multipart
    pyyaml
    jinja2
  ];
  
  # makeWrapper build tool for script wrapping
  nativeBuildInputs = [ pkgs.makeWrapper ];
  
  # my custom build phase
  installPhase = ''
    # binaries dir
    mkdir -p $out/bin
    
    # app copying
    cp app.py $out/bin/python-info-service
    
    # make bin executable
    chmod +x $out/bin/python-info-service
    
    # wrapp script with python interpreter to directly execute
    # ./result/bin/python-info-service
    wrapProgram $out/bin/python-info-service \
      --prefix PYTHONPATH : "$PYTHONPATH"
  '';
  
  # pkg description
  meta = with pkgs.lib; {
    description = "Python Info Service - FastAPI application for course lab";
    homepage = "https://github.com/projacktor/DevOps-Core-Course";
    license = licenses.mit;
    maintainers = [ projacktor ];
  };
}