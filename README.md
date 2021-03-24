# BERT entitás felismerés Azure Machine Learning, illetve Azure Kubernetes Service környezetben

Az szkript az általunk jelenleg legjobbnak vélt megoldást tartalmazza, Named Entity Recognition, entitásfelismerés célfeladatra.

Az előtanított BERT modellt (bert-base-multilingual-cased) így a megoldással finomhangolni lehet entitásfelismerésre.

Annotált szövegkorpusz a [NerKor](https://github.com/dlt-rilmta/NerKor/tree/main/data/wikipedia/morph) korpuszból általunk válagotatt szövegeket tartalmazza.

## Futtatás AzureML platformon

Futtatáshoz STANDARD_NC6S_V3 virtuális gépet ajánluk, amin AzureML platformon egy terminált nyitva le tudjuk klónozni ezt a repozitóriumot.

Ekkor a konfigurációt a config.json fájlban találjuk meg. A konfiguráció alapbeállításokkal van beállítva, amit nem szükséges (bár lehet) módosítani egy kész tanításhoz.

Ha átnéztük a konfigurációs fájlt és számunkra jónak találtuk, akkor elindíthatjuk a megoldást:

```bash
python3 run_ner.py config.json
```

Ekkor a kész modellt, ha másképp nem csináltuk, a model mappába menti a szkript.

## Docker képfájl készítése

A model mappa tartalmaz egy alap vázat, amit Docker használata segítségével buildelni tudunk, majd AKS-be feltölteni.

Ha megtörtént a finomhangolás futtatása és megelégszünk a model könyvtárban lévő webes végpont funkcionalitásával, akkor nincs más tennivalónk, mint betallózni terminálból a model könyvtárba és feltelepített [Docker](https://www.docker.com) engine esetén, kiadni a következő parancsot:

```bash
docker build -t bert-entity-recognizer:v1 .
```

Ekkor lokálisan készítettünk egy Docker képfájlt, amit futtatva egy entitásfelismerő webszolgáltatást kapunk.

## Azure Container Registry

Ahhoz, hogy deployolni tudjuk a már elkészített képfájlunkat, először fel kell töltenünk "valahova", ami az Azure Container Registry (ACR) szolgáltatása. Innen fogjuk tudni később az AKS klaszterünkből meghívni a képfájlt.

Ehhez egy felettébb hasznos linket találunk [itt](https://docs.microsoft.com/hu-hu/azure/container-registry/container-registry-get-started-portal), ahol lényegben a portal.azure.com-on kattingatva végig tudunk menni egy registry készítésén és ha ezzel megvagyunk, nem kell mást tennünk, mint a Docker képfájlukat feltagelnünk:

```bash
docker tag bert-entity-recognizer:v1 mycontainerregistry.azurecr.io/bert-entity-recognizer:v1
```

illetve ezt az ACR-be feltöltenünk:

```bash
docker push mycontainerregistry.azurecr.io/bert-entity-recognizer:v1
```

Fontos, hogy ahogy a leírás is mutatja, az "az" paranccsal közben bejelentkezve kell legyünk a terminálban, ahonnan feltöltjük a képfájlt!

Ha ezzel megvolnánk, jöhet a következő lépés.

## Azure Kubernetes Service

Ezen a ponton érdemes végigböngészni [ezt](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster) a leírást.

Legegyszerűbb módon, ha szeretnénk létrehozni egy AKS klasztert, azt a következő paranccsal tehetjük meg:

```bash
az aks create \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --node-count 2 \
    --generate-ssh-keys \
    --attach-acr acrName
```

Ahol az acrName paraméter a már elkészített Azure Container Registry neve.

Ha ezzel megvolnánk, lényegében nincs is más dolgunk, mint a model/acr-bert-entities.yaml fájlban módosítjuk a feltöltött képfájl elérési útját ACR-ben és ez után kiadni a 

```bash
kubectl apply -f acr-bert-entities.yaml
```

parancsot. Ha mindent jól csináltunk, akkor megjelenik az AKS klaszterünkben a feltöltött megoldás. Hurrá! :)

Ezután nincs más dolgunk, mint a nagyvilág felé megnyitni a szolgáltatásunk a következő paranccsal:

```bash
kubectl expose deployment bert-entity-recognizer-deployment --type=LoadBalancer --name=bert-entity-recognizer-service
```

Ekkor a 

```bash
kubectl get services
```

paranccsal, egy pár perc után le tudjuk kérdezni az AKS-ben futó webszolgáltatásunk adatait, mint a külső IP cím! :)