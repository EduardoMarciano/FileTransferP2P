function DefineTamanho(tamanho) {
  var kilobyte = 1024;
  var megabyte = 1024**2;
  var gigabyte = 1024**3;

  if (tamanho < kilobyte) {
    return tamanho + ' B';
  }
  else if (tamanho < megabyte) {
    return (tamanho / kilobyte).toFixed(2) + ' KB';
  }
  else if (tamanho< gigabyte){
    return (tamanho / megabyte).toFixed(2) + ' MB';
  }
  else{
    return (tamanho / gigabyte).toFixed(2) + ' GB';
  }
}
function sendArchives() {
  var table = document.getElementById("tbody");
  var lines = table.getElementsByTagName("tr").length;
  var chaveSender = document.getElementById("chaveS").value;

  if (lines == 0) {
    alert("Selecione um arquivo para ser enviado.");
  } else if (chaveSender == '') {
    alert("A chave identificadora deve ser selecionada.");
  } else {
    // enviar arquivos
  }
    
}

function downloadArchives() {
  var table = document.getElementById("tbodyReceiver");
  var lines = table.getElementsByClassName("checkbox");
  var isChecked = [];

  console.log(lines);

  for (var i = 0; i < lines.length; i++) {
    isChecked.push(lines[i].checked);
  }
  
  if (!isChecked.includes(true)) {
    alert("Selecione um arquivo para ser baixado.")
  } else {
    for (var i = 0; i < lines.length; i++) {
      if (lines[i].checked) {
        //download o value
        //fazer mais um for, pois a variável lines só tem os checkboxes
      }

      document.getElementById("chaveR").value = '';
      var table = document.querySelector('#fileTableReceiver tbody');
      lines = table.getElementsByTagName('tr');

      for (var i = 0; i < lines.length; i++) {
        table.removeChild(lines[i]);
      }
          
    }
  }
  
}

function pesquisar() {
  var codigoSender = document.getElementById("chaveR").value;

  if (codigoSender == '') {
    alert("Digite o código do Sender.");
  } else {
    //Vai encontrar o sender e pegar os documentos dele
    //Para testar o visual, vou usar um file qualquer
    var files = [["teste", "15KB"]];
  
    var tabela = document.querySelector('#fileTableReceiver tbody');
    
    for (var i = 0; i < files.length; i++) {
      var file = files[i][0];
      var size = files[i][1];

      var row          = document.createElement('tr');
      var nome         = document.createElement('td');
      var tamanho      = document.createElement('td');
      var action       = document.createElement('td');
      var selecionar   = document.createElement('input');
    
      nome.textContent = file;
      tamanho.textContent = size;
    
      selecionar.setAttribute("type", "checkbox");
      selecionar.setAttribute('class', "checkbox");
      selecionar.style.cursor = 'pointer';      

      action.append(selecionar);

      row.appendChild(nome);
      row.appendChild(tamanho);
      row.appendChild(action);
    
      tabela.appendChild(row);
    }
  }
}

document.getElementById('myfile').addEventListener('change', function(evento) {

  var files = evento.target.files;
  var tabela = document.querySelector('#fileTable tbody');

  tabela.innerHTML = '';

  for (var i = 0; i < files.length; i++) {
    var file = files[i];

    var row          = document.createElement('tr');
    var nome         = document.createElement('td');
    var tamanho      = document.createElement('td');
    var action       = document.createElement('td');
    var excluir      = document.createElement('button');

    nome.textContent = file.name;
    tamanho.textContent = DefineTamanho(file.size);

    excluir.textContent = 'Excluir';
    excluir.setAttribute('data-index', i);
    excluir.style.cursor = 'pointer'; 
    excluir.addEventListener('click', function(evento) {
      
      tabela.removeChild(evento.target.parentNode.parentNode);

    });
    action.appendChild(excluir);

    row.appendChild(nome);
    row.appendChild(tamanho);
    row.appendChild(action);
    
    tabela.appendChild(row);
  }

});