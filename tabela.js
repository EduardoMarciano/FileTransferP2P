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