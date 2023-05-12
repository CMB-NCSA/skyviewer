# NCSA SkyViewer

## HiPS file generation

Useful resources:

* [HiPS in 10 steps](https://aladin.cds.unistra.fr/hips/HipsIn10Steps.gml) - basics of HiPS generation
* [Hipsgen manual](https://aladin.cds.unistra.fr/hips/HipsgenManual.pdf) 

HiPS generation requires Aladin.jar (provided in this repository).



## AladinLite API basics


## Development

For the sake of convenience, we are using [the JupyterHub instance](https://gitlab.com/gasc-ncsa/kubernetes/-/blob/master/apps/root/templates/jupyterhub.yaml) deployed [on the SPT-3G Kubernetes cluster](https://spt3g.ncsa.illinois.edu/argo-cd/applications/jupyterhub) for development of the SkyViewer source code. A personal JupyterLab server can be [launched here](https://jupyter.gasc.ncsa.illinois.edu/).

One of the reasons we are developing this way is that the JupyterHub instance already [includes a mounted volume from the high-capacity Taiga storage system](https://gitlab.com/gasc-ncsa/kubernetes/-/blob/master/apps/root/values.yaml). The data files can be generated via JupyterLab and served by an independent [NGINX webserver](https://gitlab.com/spt3g/kubernetes/-/blob/main/charts/skyviewer/templates/deployment.yaml) *in situ*.

The [JupyterLab server image is a custom build](./Dockerfile) that includes the required development libraries and tools.

## Deployment

The NCSA SkyViewer web app is deployed [via ArgoCD](https://spt3g.ncsa.illinois.edu/argo-cd/applications/skyviewer) on our SPT-3G Kubernetes cluster. There is [a Helm chart](https://gitlab.com/spt3g/kubernetes/-/tree/main/charts/skyviewer) driving [the ArgoCD Application](https://gitlab.com/spt3g/kubernetes/-/blob/main/apps/spt3g/templates/skyviewer.yaml).

## Access control

### JupyterLab server

Access to the JupyterHub service requires membership in the group `/gasc/jupyterhub` in [the "GASC" realm of our SPT-3G project Keycloak server](https://keycloak.spt3g.ncsa.illinois.edu/realms/GASC/).

### SkyViewer web app

The SkyViewer ArgoCD Application referenced in the Deployment section includes an instance of [OAuth2-Proxy](https://gitlab.com/decentci/charts/-/tree/main/charts/oauth2-proxy-traefik), which provides a lightweight middleware to secure arbitrary ingress routes. In this case, it is configured to authenticate visitors using [the "CAPS" realm of our SPT-3G project Keycloak server](https://keycloak.spt3g.ncsa.illinois.edu/realms/caps/). Access to the SkyServer web app at https://skyviewer.caps.ncsa.illinois.edu/map/ is limited to members of the Keycloak group `/caps/skyviewer` as [configured in the ArgoCD Application](https://gitlab.com/spt3g/kubernetes/-/blob/1dbf960c376c5dafcdfa253ec695697bb173b110/apps/spt3g/values.yaml#L13).
