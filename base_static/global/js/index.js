function altera_quantidade(){
  let item = document.getElementById('id_pk_item');
  let programacao = document.getElementById('id_programacao');
  let qtde = document.getElementById('id_quantidade');
  let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
  

  let id_item = item.value;
  let id_programacao = programacao.value;
  let qtde_alterada = qtde.value;

  data = new FormData()
  data.append("id_item", id_item)
  data.append('id_programação', id_programacao)
  data.append('qtde_alterada',qtde_alterada)
  

  fetch("/order/quantidade/",{
    method:'POST',
    headers:{
      'X-CSRFToken': csrf_token,
    },
    body: data,

  }).then(function(result){
    return result.json()
  }).then(function (data) {
    if (data.is_altered){
      let answer = window.confirm('Deseja alterar quantidade\nde Subitens Programados?')
        if (answer){
          const litaSubitens = document.getElementById('lista_subitens_id');
          const itens = litaSubitens.querySelectorAll('li');
          const pks = [];

          itens.forEach(item=>{
            const pk = item.dataset.pk;
            pks.push(pk);
          })

          fetch('/order/alterqtde/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
              pks: pks,
              n_qtde: qtde_alterada,
              id_item: id_item,
            })
          })
          .then(function(result){
            return result.json()
          }).then(data2 => {

            const vlr_list = JSON.parse(data2);

            for (let i=0; i < vlr_list.length; i++){
              const nova_quantidade = vlr_list[i];
              idElemento = `${nova_quantidade.pk}`;
              subitem = document.getElementById(idElemento);
              subitem.textContent = nova_quantidade.qtde;
            };
          })
          .catch(error => {
            console.error('Erro:', error);
          });
        } 
    }})
  }


// function start_setup(){
//   const barcode_element = document.getElementById("barcode_inicial");
//   const barcode_value = barcode_element.value;

//   const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
//   const maquina_id = document.getElementById("id_machine").value;
  
//   data = new FormData();
//   data.append("barcode_value", barcode_value);
//   data.append("maquina_id",maquina_id);
  

//   fetch ('/apont/setup/',{
//     method: 'POST',
//     headers:{
//       'X-CSRFToken': csrf_token,
//     },
//     body: data,
//   }).then(function(result) {
//     return
//   }).then(data => {
//     return
//   })

// }


function iniciar_producao(){
  const aponta_container = document.getElementById(
    'aponta_container').style.display = 'flex';

  const id_apont = document.getElementById("id_apont").value;
  const maquina_id = document.getElementById("id_machine").value;
  let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const radio_selected = document.querySelectorAll('input[name="flexRadioDefault"]');
  const motive_selected = document.getElementById('apont_motive');
  const maquina_name = document.getElementById("name_machine").value
  let radio_value = '';
  let motive_value = '';

  for (const radio of radio_selected) {
    if(radio.checked){
      radio_value = radio.value;
    }
    if (radio.id === 'id_Retrabalho') {
      if(motive_selected.value){
        motive_value = motive_selected.value
      }}}

  data = new FormData();
  data.append('id_apont',id_apont);
  data.append("maquina_id",maquina_id);
  data.append('apont_type', radio_value);
  data.append('motive_value', motive_value);
  data.append('maquina_name', maquina_name);




  fetch ('/apont/start-setup/',{
    method: 'POST',
    headers:{
      'X-CSRFToken': csrf_token,},
    body: data,
    
  }).then(function(result) {
    const btn_iniciar = document.getElementById('iniciar_producao')
    const div_btn = document.getElementById('iniciar_container')
    const maquina_name = document.getElementById("name_machine").value

      btn_iniciar.removeAttribute('onclick')
      btn_iniciar.classList.replace('btn-success','btn-secondary')
      btn_iniciar.classList.remove('link_extra')

      div_btn.classList.remove('h_6')

      // Função para alterar o status da máquina
      function alterarStatus(maquinaId, novoStatus) {
        localStorage.setItem(`status_${maquinaId}`, novoStatus);
        if (novoStatus === 'producao') {
          localStorage.setItem(`tempoParada_${maquinaId}`, 0);
        }else if(novoStatus === 'setup'){
          localStorage.setItem(`tempoParada_${maquinaId}`, 0);
        }
      }

      alterarStatus(maquina_name,'producao')

    return
  }).then(data => {
    return
  })
}


function fim_producao() {
  const qtde_boa = document.getElementById("qtde_boa");
  const qtde_ruim = document.getElementById("qtde_ruim");
  const id_apont = document.getElementById("id_apont").value;
  const maquina_id = document.getElementById("id_machine").value;

  let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

  data = new FormData();
  data.append('qtde_boa', qtde_boa.value);
  data.append('qtde_ruim', qtde_ruim.value);
  data.append('id_apont',id_apont);
  data.append("maquina_id",maquina_id);

  fetch ('/apont/fim_producao/',{
    method: 'POST',
    headers:{
      'X-CSRFToken': csrf_token,
    },
    body: data,
  }).then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
  }).then(data => {
    // Lidar com a resposta do servidor, se necessário
    console.log('Dados enviados com sucesso:', data);
    // Redirecionar para a página inicial (opcional, pois o Django já pode fazer isso)
    window.location.href = '/apont/';
})
.catch(error => {
  console.log('There has been a problem with your fetch operation:', error);

});
}
