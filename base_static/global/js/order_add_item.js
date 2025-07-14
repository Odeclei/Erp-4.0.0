function exibir_form_add_item(tipo) {
  add_item = document.getElementById('form-add-item')
  
  if (tipo == 1) {
    add_item.style.display = 'block';
  }else if (tipo == 0){ 
    add_item.style.display = 'none';

    // item = document.getElementById('select2-id_item-container');
    // item.value='';
    quantidade = document.getElementById('id_quantidade');
    quantidade.value="";
    start_at = document.getElementById('id_start_at');
    start_at.value = "";
    ends_at = document.getElementById('id_ends_at');
    ends_at.value = "";
  }}
