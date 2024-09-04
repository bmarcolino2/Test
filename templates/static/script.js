function mostrarCatalogo() {
    document.getElementById('catalogo').classList.add('ativa');
    document.getElementById('carrinho').classList.remove('ativa');
}

function mostrarCarrinho() {
    document.getElementById('catalogo').classList.remove('ativa');
    document.getElementById('carrinho').classList.add('ativa');
}

// Exibir a página de catálogo por padrão
mostrarCatalogo();
