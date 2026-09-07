# Terminal 1 — Nós do Cluster Sync e Clientes
docker compose logs --follow --no-log-prefix `
  node0 node1 node2 node3 node4 `
  client1 client2 client3 client4 client5 2>$null |
  Where-Object { $_ -notmatch "FALHA|ERRO|HEARTBEAT|indisponível|morto|ELEIÇÃO" }
