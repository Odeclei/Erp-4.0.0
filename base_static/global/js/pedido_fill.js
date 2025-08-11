document.addEventListener("DOMContentLoaded", () => {
    const itemSearchInput = document.getElementById("item_search");
    const finishSearchInput = document.getElementById("finish_search");
    const hiddenItemInput = document.getElementById("id_item_hidden");
    const hiddenFinishInput = document.getElementById("id_finish_hidden");
    const datalisItem = document.getElementById("datalistItensOptions");
    const datalistFinish = document.getElementById("datalistFinishOptions");
    const observationInput = document.getElementById("id_observation");

    const lista_code_chemure = {
        "44-1": "MDT1711-2",
        "45-1": "MDT1711-1",
        "46-1": "MD1311-2",
        "47-1": "MD1311-1",
        "48-1": "MD1411-2",
        "49-1": "MD1411-1",
        "50-1": "MD2201-2",
        "51-1": "MD2211-1",
        "52-1": "MD1011",
        "44-2": "MDT1703-2",
        "45-2": "MDT1703-1",
        "46-2": "MD1303-2",
        "47-2": "MD1303-1",
        "48-2": "MD1403-2",
        "49-2": "MD1403-1",
        "50-2": "MD2203-2",
        "51-2": "MD2203-1",
        "52-2": "MD1003",
        "44-3": "MDT1712-2",
        "45-3": "MDT1712-1",
        "46-3": "MD1312-2",
        "47-3": "MD1312-1",
        "48-3": "MD1412-2",
        "49-3": "MD1412-1",
        "50-3": "MD2212-2",
        "51-3": "MD2212-1",
        "52-3": "MD1012",
        "44-4": "MDT1309-2",
        "45-4": "MDT1309-1",
        "46-4": "MD1309-2",
        "47-4": "MD1309-1",
        "48-4": "MD1409-2",
        "49-4": "MD1409-1",
        "50-4": "MD2209-2",
        "51-4": "MD2209-1",
        "52-4": "MD1009",
    };

    let itemValue = "";
    let finishValue = "";

    itemSearchInput.addEventListener("input", function (event) {
        const inputValue = event.target.value;
        const option = Array.from(datalisItem.options).find(
            (opt) => opt.value === inputValue
        );
        if (option) {
            const pk = option.getAttribute("data-pk");
            hiddenItemInput.value = pk;
            itemValue = pk;
            verificaValores();
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
            finishValue = pk;
            verificaValores();
        } else {
            hiddenFinishInput.value = "";
        }
    });

    function verificaValores() {
        if (itemValue !== "" && finishValue !== "") {
            const chave = `${itemValue}-${finishValue}`;

            if (lista_code_chemure[chave]) {
                const valorDaLista = lista_code_chemure[chave];
                observationInput.value = valorDaLista;
            } else {
            }
        } else {
            observationInput.value = "";
        }
    }
});
