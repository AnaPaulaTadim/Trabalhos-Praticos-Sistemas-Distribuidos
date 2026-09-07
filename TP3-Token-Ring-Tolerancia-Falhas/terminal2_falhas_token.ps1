# Terminal 2 — Falhas, Heartbeat e Token Ring
docker compose logs --follow --no-log-prefix `
  node0 node1 node2 node3 node4 2>$null |
  Where-Object { $_ -match "FALHA|ERRO|HEARTBEAT|indisponível|morto|ELEIÇÃO|pulado|FAILOVER|detectado|Assumindo|reintegrado" }
