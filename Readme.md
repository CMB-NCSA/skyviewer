# NCSA SkyViewer

## HiPS file generation

Useful resources:

* [HiPS in 10 steps](https://aladin.cds.unistra.fr/hips/HipsIn10Steps.gml) - basics of HiPS generation
* [Hipsgen manual](https://aladin.cds.unistra.fr/hips/HipsgenManual.pdf) 

HiPS generation requires ```Aladin.jar``` (provided in this repository).

To generate HiPS with default options run a command:
```java -Xmx16g -jar AladinBeta.jar -hipsgen in=Data out=PilotHiPS id=HiPSID```
Notes:
* ```-Xmx16g``` defines memory allocation (16Gb)
* ```inData``` is a directory with files to convert (tiles in single band)
* ```out``` is a name of output directory
* ```id``` matters more if we want to add HiPS to public pool

Other options that might be useful:
* ```blank=0``` - this parameters is set to ```null``` by default. Switching it to 0 makes hipsgen to switch all zero values with null and make the image transparent where there is no scientific data.
* ```"dataRange=-0.1 0.1"``` - defines useful data range
* ```"pixelCut=min max [fct]"``` parameter allows to explicitly indicate the range of original values to be taken into account and the "transfer function" to be applied to obtain the 255 possible values of the compressed tiles: log, sqrt, linear (default), asinh, pow2. 
* ```color=jpeg``` generate JPEGs instead of PNGs (default).


## AladinLite API basics

Useful resources:
* [AladinLite API examples](https://aladin.u-strasbg.fr/AladinLite/doc/API/examples/)
* [AladinLite simple tutorial](https://aladin.cds.unistra.fr/AladinLite/doc/tutorials/interactive-finding-chart/)

## Development using JupyterHub

A [dedicated JupyterHub instance that can be launched here 🔒](https://jupyter.skyviewer.ncsa.illinois.edu/) is available for development of the SkyViewer source code.

One of the reasons we are developing this way is that the JupyterHub instance already [includes a mounted volume from the high-capacity Taiga storage system](https://gitlab.com/spt3g/kubernetes/-/blob/main/charts/jupyterhub/values.yaml). The data files can be generated via JupyterLab and served by an independent [NGINX webserver](https://gitlab.com/spt3g/kubernetes/-/blob/main/charts/skyviewer/templates/deployment.yaml) *in situ*.

The [JupyterLab server image is a custom build](./docker/jupyter/Dockerfile) that includes the required development libraries and tools.

## Development using Docker locally

### Build the Aladin Lite image

Change to the root directory of your clone of this repo and do the following as shown below:

* Clone our Aladin Lite source repo fork (`develop` branch).
* Build the Docker container image.
* Run the Docker container to verify that the JavaScript works.

```bash
$ git clone -b develop git@github.com:CMB-NCSA/aladin-lite.git aladin-lite

$ docker build ./aladin-lite -t registry.gitlab.com/cmb-ncsa/aladin-lite

$ docker run --rm -it -p 8088:8088 registry.gitlab.com/cmb-ncsa/aladin-lite

> aladin-lite@3.1.0 serve
> vite --host --port 8088


  VITE v4.3.9  ready in 315 ms

  ➜  Local:   http://localhost:8088/
  ➜  Network: http://172.17.0.2:8088/
  ➜  press h to show help

```

Open your browser to http://localhost:8088/examples/.

### Workflow for iterating on Aladin Lite JavaScript

To iterate on code:

1. Edit `www/index.html` and any other web files comprising the web app under `www/`
2. Edit Aladin source files under `aladin-lite/src/`
3. Run the `build_aladin.sh` script to rebuild the JavaScript file and copy into `www/js/`
4. Repeat steps 1-3.

## Deployment

The NCSA SkyViewer web app is deployed [🔒 via ArgoCD](https://spt3g.ncsa.illinois.edu/argo-cd/applications/skyviewer) on our SPT-3G Kubernetes cluster. There is [a Helm chart](https://gitlab.com/spt3g/kubernetes/-/tree/main/charts/skyviewer) driving [the ArgoCD Application](https://gitlab.com/spt3g/kubernetes/-/blob/main/apps/spt3g/templates/skyviewer.yaml).

The JupyterHub instance is also deployed [🔒 via ArgoCD](https://spt3g.ncsa.illinois.edu/argo-cd/applications/jupyterhub-skyviewer), using [this Helm chart](https://gitlab.com/spt3g/kubernetes/-/tree/main/charts/jupyterhub) that drive [this ArgoCD Application](https://gitlab.com/spt3g/kubernetes/-/blob/main/apps/spt3g/templates/jupyterhub.yaml).

## Access control

### SkyViewer web app

The SkyViewer ArgoCD Application referenced in the Deployment section includes an instance of [OAuth2-Proxy](https://gitlab.com/decentci/charts/-/tree/main/charts/oauth2-proxy-traefik), which provides a lightweight middleware to secure arbitrary ingress routes. In this case, it is configured to authenticate visitors using [the "spt3g" realm of our SPT-3G project Keycloak server](https://keycloak.spt3g.ncsa.illinois.edu/realms/spt3g/). Access to the SkyServer web app at https://skyviewer.ncsa.illinois.edu/map/ is limited to members of the Keycloak group `/skyviewer` as configured in its ArgoCD Application linked above.

### JupyterLab server

Access to the JupyterHub service requires membership in the group `/caps/jupyterhub` in [the "caps" realm of our SPT-3G project Keycloak server](https://keycloak.spt3g.ncsa.illinois.edu/realms/caps/). Membership in the group `/caps/jupyterhub/admin` grants users access to the [🔒 JupyterHub admin control panel](https://jupyter.skyviewer.ncsa.illinois.edu/hub/admin).
