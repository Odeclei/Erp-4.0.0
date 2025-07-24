document.addEventListener("DOMContentLoaded", () => {
    const itemSearchInput = document.getElementById("item_search");
    const finishSearchInput = document.getElementById("finish_search");
    const hiddenItemInput = document.getElementById("id_item_hidden");
    const hiddenFinishInput = document.getElementById("id_finish_hidden");
    const datalisItem = document.getElementById("datalistItensOptions");
    const datalistFinish = document.getElementById("datalistFinishOptions");

    itemSearchInput.addEventListener("input", function (event) {
        const inputValue = event.target.value;
        const option = Array.from(datalisItem.options).find(
            (opt) => opt.value === inputValue
        );
        if (option) {
            const pk = option.getAttribute("data-pk");
            hiddenItemInput.value = pk;
        } else {
            hiddenItemInput.value = "";
        }
    });

    finishSearchInput.addEventListener("input", function (event) {
        const inputValue = event.target.value;
        const option = Array.from(datalistFinish.options).find(
            (opt) => opt.value === inputValue
        );
        if (option) {
            const pk = option.getAttribute("data-pk");
            hiddenFinishInput.value = pk;
        } else {
            hiddenFinishInput.value = "";
        }
    });
});

function finalizarEdicao() {
    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;
    console.log("Iniciando finaliza o de edicao");
    console.log("csrfToken:", csrfToken);

    $.ajax({
        type: "GET",
        url: "{% url 'pedidos:finalizar_edicao' pedido.pk %}",
        success: function (data) {
            console.log("finalizarEdicao() success callback:", data);
            if (data.success) {
                console.log("Finaliza o de edicao realizada com sucesso!");
                window.location.reload();
            } else {
                console.error(
                    "Finaliza o de edicao falhou:",
                    data.message || "Erro desconhecido."
                );
            }
        },
        error: function (xhr, status, error) {
            console.error("Erro na requisi o AJAX:", status, error, xhr);
        },
    });
}

function imprimirEtiquetas() {
    const btn_print_labels = document.getElementById("btn-imprime-etiqueta");
    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;
    event.preventDefault();
    btn_print_labels.disabled = true;
    btn_print_labels.innerText = "Imprimindo...";
    $.ajax({
        type: "POST",
        url: "{% url 'pedidos:imprimir_etiquetas' pedido.pk %}",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        success: function (data) {
            console.log(data);
            if (data.success) {
                console.log("Etiquetas impressas com sucesso.");
            } else {
                console.error(
                    "Finalização da edição falhou:",
                    data.message || "Erro desconhecido."
                );
            }
        },
        error: function (xhr, status, error) {
            console.error("Erro na requisição AJAX:", status, error, xhr);
        },
    });
}
