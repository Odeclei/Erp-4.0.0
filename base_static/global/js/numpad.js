const numBtns = document.querySelectorAll('.container button');
// const operatorBtns = document.querySelectorAll('.numpad .operator-button');
const pcboaInput = document.getElementById('qtde_boa');
const pcruimInput = document.getElementById('qtde_ruim');

let currentInput = pcboaInput; // Campo selecionado inicialmente
let currentValue = ''; // Valor digitado

pcruimInput.addEventListener('click',() =>{
  currentInput = pcruimInput
  currentValue = ''
})

numBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    currentValue += btn.textContent;
    updateInputValue();
  });
});

// operatorBtns.forEach(btn => {
//   btn.addEventListener('click', () => {
//     if (currentValue) {
//       handleOperation(currentValue, btn.textContent);
//       currentValue = '';
//     }
//   });
// });

pcboaInput.addEventListener('focus', () => {
  currentInput = pcboaInput;
});

pcruimInput.addEventListener('focus', () => {
  currentInput = pcruimInput;
});

function updateInputValue() {
  currentInput.value = currentValue;
}
