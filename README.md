# Green — companheiro virtual

Pequeno robô em pixel art. **Estado atual: ETAPA 1 (personagem e aparência).**

## Como executar (VS Code)
1. Abra a pasta `GREEN` no VS Code (Arquivo > Abrir Pasta).
2. Instale a extensão **Live Server** (Ritwick Dey).
3. Clique com o botão direito em `frontend/index.html` > **Open with Live Server**.

Alternativa sem extensão: dê dois cliques em `frontend/index.html`.

## Regenerar os sprites (opcional)
```
pip install pillow
python tools/gerar_sprites.py
```

## Estrutura
- `frontend/index.html` — estrutura da página
- `frontend/style.css` — visual minimalista (quadrado branco, menu, painéis)
- `frontend/script.js` — animações, menu e interações iniciais
- `frontend/assets/sprites/` — sprites PNG do Green (fundo transparente)
- `tools/gerar_sprites.py` — gera os sprites a partir de código
- `backend/`, `desktop/`, `mobile/` — pastas reservadas para as próximas etapas
