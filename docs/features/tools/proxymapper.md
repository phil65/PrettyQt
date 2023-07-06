::: prettyqt.itemmodels.ProxyMapper


When having a complex proxy tree like:

``` mermaid
classDiagram
  Shared_proxy <|-- Proxy_1_1
  Shared_proxy <|-- Proxy_2_1
  Proxy_1_1 <|-- Proxy_1_2
  Proxy_2_1 <|-- Proxy_2_2
  Root_model <-- Shared_proxy
  class Proxy_1_1{
  }
  class Proxy_2_1{
  }
  class Root_model{
  }
```

then the ProxyMapper can be used to map indexes and ItemSelections easily between any of the proxies.

``` py
mapper = ProxyMapper(proxy_1_2, proxy_2_1)
index = proxy_1_2.index(0, 0)
mapped_index = mapper.map_index(source=0, target=1, index)
```

The mapper will find the closest parent ("shared_proxy" here),
use mapToSource / mapSelectionFromSource until it gets there,
and then use mapFromSource / mapSelectionFromSource to get down to 2_1.

