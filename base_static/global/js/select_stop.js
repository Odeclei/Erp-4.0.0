function select_group(id_category){
  data = new FormData();
  data.append("id_category", id_category)

  fetch("/apont/subgrupo_stop/",{
    method:'POST',
    headers:{},
    body: data,
  }).then(function(result){
    return result.json()

  }).then(function(data) {
    const section_grupo = document.getElementById('stop_group');
    const section_subgrupo = document.getElementById('stop_subgrupo');
    
    section_grupo.style.display = "none";
    section_subgrupo.style.display = "block";
    section_subgrupo.innerHTML = ""
    section_subgrupo.innerHTML = "\
    <div id='div_subgrupo'class='mt-3 d-flex justify-content-center'>\
    </div>"

    const div_subgrupo = document.getElementById('div_subgrupo')

    for (i = 0; i < data.length; i++) {
      div_subgrupo.innerHTML +=

      "\
      <div class='card d-flex mt-1 ml-1 mb-1 ml-1' style='width: 25rem; cursor: pointer'>\
        <div onclick='select_subgroup("+data[i]['id']+")' class='card-body d-flex df-center '>\
          <h3 class='card-title'>"+data[i]['fields']['name']+"</h3>\
          </div>\
      </div>"
    }
    section_subgrupo.innerHTML += "\
    <div class='d-flex justify-content-center mt-4'><br>\
      <input type='button' value='Voltar' class='btn btn-lg btn-secondary' onclick='back_grupo()'>\
    </div>"
  })
}

function back_grupo() {
  const section_grupo = document.getElementById('stop_group');
  const section_subgrupo = document.getElementById('stop_subgrupo');
  
  section_grupo.style.display = "flex";
  section_subgrupo.style.display = "none";
}

function select_subgroup(id_sub){
  const hr_parada = document.getElementById("hr_parada");
  const id_machine = document.getElementById("id_machine");
  const name_machine = document.getElementById("name_machine");


  data = new FormData();
  data.append("motive_id",id_sub)
  data.append('hr_parada',hr_parada.value)
  data.append('id_machine',id_machine.value)
  data.append('name_machine',name_machine.value)

  fetch("/apont/apont_stop/",{
    method:'POST',
    headers:{},
    body: data,
  }).then(function(result){
    return result.json()
  }).then(function(data){

    
    function tempoOEE(novoTempo){
      const hoje = new Date().toISOString().slice(0,10);
      const chaveLocalStorage = `tempo_total_${hoje}`;
      

      let tempoTotal = localStorage.getItem(chaveLocalStorage);

      if(tempoTotal){
        tempoTotal = parseInt(tempoTotal,10) + novoTempo;
      }else{
        tempoTotal = novoTempo;
      }
      localStorage.setItem(chaveLocalStorage,tempoTotal)
    }
    tempoOEE(data.timestop)

    if(data.apont ==='ok'){
        window.close()
      }else{
        alert("Ocorreu um erro ao salvar Parada")
      }
      localStorage.setItem(`tempoParada_${name_machine.value}`,0);
      localStorage.setItem(`restart_${name_machine.value}`,'restart');
    }
    
  )
}
