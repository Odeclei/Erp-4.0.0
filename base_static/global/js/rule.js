const modal = document.getElementById("modal-cadastro");
const btnAbrirModal = document.getElementById("btn-abrir-modal");
const btnFechar = document.querySelector(".fechar");

const passo1 = document.getElementById("passo-1");
const passo2 = document.getElementById("passo-2");
const passo3 = document.getElementById("passo-3");

const selectGrupo = document.getElementById("select-grupo");
const selectSetor = document.getElementById("select-setor");
const inputNome = document.getElementById("input-nome");

//1. abrir e fechar o Modal
btnAbrirModal.onclick = function () {
    modal.style.display = "flex";
    document.body.classList.add("modal-open");
    carregarGrupos();
};
btnFechar.onclick = function () {
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
};
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
    }
};

//2. Carregar os Grupos d Banco de Dados
async function carregarGrupos() {
    try {
        const response = await fetch("/regras/api/grupos/");
        const grupos = await response.json();

        selectGrupo.innerHTML =
            '<option value=""> -- Selecione um Grupo -- </option>';
        grupos.forEach((grupo) => {
            const option = document.createElement("option");
            option.value = grupo.id;
            option.textContent = grupo.name;
            selectGrupo.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar grupos:", error);
    }
}

//3. Logica de Navegação entre os Passos
document.getElementById("btn-passo-1").onclick = async function () {
    const grupoId = selectGrupo.value;
    if (!grupoId) {
        alert("Selecione um Grupo");
        return;
    }
    // Carrega os setores dinamicamente
    await carregarSetores(grupoId);
    passo1.style.display = "none";
    passo2.style.display = "block";
};

document.getElementById("btn-passo-2").onclick = function () {
    if (!selectSetor.value) {
        alert("Selecione um Setor");
        return;
    }
    passo2.style.display = "none";
    passo3.style.display = "block";
};

//4. Funções de navegação "voltar"
document.getElementById("btn-voltar-1").onclick = function () {
    passo2.style.display = "none";
    passo1.style.display = "block";
};
document.getElementById("btn-voltar-2").onclick = function () {
    passo3.style.display = "none";
    passo2.style.display = "block";
};

//5. Função para Carregar os Setores(Chamada via Ajax)
async function carregarSetores(grupoId) {
    try {
        const response = await fetch(`/regras/api/grupos/${grupoId}/setores/`);
        const setores = await response.json();

        selectSetor.innerHTML =
            '<option value=""> -- Selecione um Setor -- </option>';
        setores.forEach((setor) => {
            const option = document.createElement("option");
            option.value = setor.id;
            option.textContent = setor.name;
            selectSetor.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar setores:", error);
    }
}

//6. Enviar o Formulario para a API(Último Passo)
document.getElementById("btn-finalizar").onclick = async function () {
    const setorId = selectSetor.value;
    const nomePosto = inputNome.value;

    console.log("id setor: ", setorId);
    console.log("nome posto: ", nomePosto);

    if (!setorId || !nomePosto) {
        alert("Preencha todos os campos");
        return;
    }

    const dados = {
        setor_id: setorId,
        nome_posto: nomePosto,
    };
    try {
        const response = await fetch("/regras/api/cadastrar_posto/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(dados),
        });

        const resultado = await response.json();

        if (response.ok) {
            alert(resultado.message);
            modal.style.display = "none";
            passo1.style.display = "block";
            passo2.style.display = "none";
            passo3.style.display = "none";
            inputNome.value = "";
            window.location.reload();
        } else {
            alert("Erro ao cadastrar posto de trabalho: " + resultado.error);
        }
    } catch (error) {
        console.error("Erro ao cadastrar posto de trabalho:", error);
        alert("Ocorreu um erro ao tentar cadastrar o posto.");
    }
};
