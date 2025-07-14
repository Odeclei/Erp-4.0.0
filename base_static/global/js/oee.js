
  var showTime=() => {
    function disponibility(){
      function zeroAEsquera (num){
        return num>=10 ? num : `0${num}`;
      }

      function formataHora(hora){
        const horabr = zeroAEsquera(hora.getHours());
        const minbr = zeroAEsquera(hora.getMinutes());
        const segbr = zeroAEsquera(hora.getSeconds());
        
        return`${horabr}:${minbr}:${segbr}`
      }

        const hrInicioTurno = new Date()
        hrInicioTurno.setHours(7, 0, 0, 0); // Configura a hora para 7h
        const hrAtual = new Date();
        const hrStartToString = formataHora(hrInicioTurno);
        const hratualToString = formataHora(hrAtual);
        const timeElapsed = hrAtual - hrInicioTurno;
        const timeLunch = 60*60*1000;   //60min convertido para milisegundos


        function timeStopped(num){
          const hrInicioAlmoço = new Date();
          const hoje = hrInicioAlmoço.toISOString().slice(0,10);
          const tempo_paradas = localStorage.getItem(`tempo_total_${hoje}`);
            
          paradas_milisegundos=tempo_paradas*1000
            
          hrInicioAlmoço.setHours(12,0,0,0)

          if (hrAtual > hrInicioAlmoço){
            const totalTimeStopped = (timeLunch+paradas_milisegundos);
            return totalTimeStopped
          } else {
            const totalTimeStopped = (paradas_milisegundos);
            return totalTimeStopped
          }
        }
        const stopped = timeStopped(hrAtual);
        const timestopped = stopped/1000/60;

        function dispIndex(stopped,timestopped,timeElapsed){
            let disponibilidadeIndex = (timeElapsed - stopped) / timeElapsed
            return disponibilidadeIndex = (disponibilidadeIndex*100).toFixed(2);
        }

        const disponibilidade = dispIndex(stopped,timestopped,timeElapsed)
        
        
        const hrInicioHtml = document.getElementById('horaInicio');
        const hrAtualHtml = document.getElementById('horaAtual');
        const disponibilidadeHtml = document.getElementById('disponibilidade');
        
        //hrInicioHtml.innerHTML = `Hora inicial: ${hrStartToString}`;
        hrAtualHtml.innerHTML = `${hratualToString}`;
        // Tempo parado: ${timestopped}`;
        disponibilidadeHtml.innerHTML =`${disponibilidade}%`;
        
        const dispIndexNumber = Number(disponibilidade);
        
        return dispIndexNumber;

    }
    function performance(){
        /*
        BUSCAR NO BANCO DE DADOS QUANTIDADE DE PEÇAS PRODUDIZA POR MÁQUINA NO 
        DIA ATUAL.
        */
        const qntyProduced = 2500; //soma de peças boas e ruins

        function hrInicioTurno(){
            const hrInicio = new Date();
            hrInicio.setHours(7,0,0,0);
            return hrInicio;
        }
        function timeAtual(){
            return (new Date());
        }
        function idealCycle(){
        //          pc/dia : 9h : 60 (min) : 60(seg) : 1000 (miliseg)
            const pcXmilisecond = 7000/9/60/60/1000;
            const timeElapsed = timeAtual()-hrInicioTurno(); // miliseconds
            const idealCycleTime = pcXmilisecond * timeElapsed;
            return idealCycleTime
        }

        const perfor = qntyProduced/idealCycle();
        const perforIndex = (perfor * 100).toFixed(2);

        const performHtml = document.getElementById('performance');
        performHtml.innerHTML = `${perforIndex}%`;

        const perforIndexNumber = Number(perforIndex)
        return perforIndexNumber

    }

    disponibility();
    performance();

    const aaa = ((disponibility()*performance())/100).toFixed(2);
    const oeeHtml = document.getElementById('OEE');
    oeeHtml.innerHTML = `${aaa}%`
  }

  setInterval(showTime,1000);


  function monitorarStatus(){
    const maquinaId = document.getElementById('name_machine');
    const name_maquina = maquinaId.value;
    const time_to_action = 30

    // localStorage.setItem(`status_${name_maquina}`, 'parada') ; //define nome do local storage, e status de parada (padrão)
    localStorage.setItem(`tempoParada_${name_maquina}`, 0);

    let status = localStorage.getItem(`status_${name_maquina}`);
    
    if (status === 'parada') {
      let contador = 0;
      
      const intervalo = setInterval(() => {
        contador++ ;
        localStorage.setItem(`tempoParada_${name_maquina}`, contador)
        let status = localStorage.getItem(`status_${name_maquina}`);
        
        if (contador >= time_to_action && status === 'parada') {
          clearInterval(intervalo);
          window.open('/apont/parada/');
        }
      },1000)
      
    } 
  }

  setInterval(() =>{
    const name_maquina = document.getElementById('name_machine').value;
    const tempoParada = localStorage.getItem(`tempoParada_${name_maquina}`);
    const restart = localStorage.getItem(`restart_${name_machine.value}`)
    if (restart === 'restart' && tempoParada == 0){
      localStorage.setItem(`restart_${name_machine.value}`,'none');
      monitorarStatus();
    }
  },1000)

  monitorarStatus();
