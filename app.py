from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agenda Sheila Nail Designer</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome para Ícones -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-light">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="#"><i class="fa-solid fa-wand-magic-sparkles text-warning"></i> Sheila Nail Designer</a>
            <span class="text-white small"><i class="fa-solid fa-location-dot me-1"></i> Capivari - SP</span>
        </div>
    </nav>

    <div class="container">
        <!-- Abas de Navegação -->
        <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="agenda-tab" data-bs-toggle="tab" data-bs-target="#agenda" type="button" role="tab"><i class="fa-solid fa-calendar-days"></i> Agendamentos</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="clientes-tab" data-bs-toggle="tab" data-bs-target="#clientes" type="button" role="tab"><i class="fa-solid fa-users"></i> Gerenciar Clientes</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="servicos-tab" data-bs-toggle="tab" data-bs-target="#servicos" type="button" role="tab"><i class="fa-solid fa-list-check"></i> Gerenciar Serviços</button>
            </li>
        </ul>

        <div class="tab-content" id="myTabContent">
            <!-- ABA 1: AGENDA -->
            <div class="tab-pane fade show active" id="agenda" role="tabpanel">
                <div class="row">
                    <!-- Formulário de Agendamento -->
                    <div class="col-md-4 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0"><i class="fa-solid fa-plus-circle"></i> Novo Agendamento</h5>
                            </div>
                            <div class="card-body">
                                <form id="formAgendamento">
                                    <div class="mb-3">
                                        <label for="cliente" class="form-label">Nome da Cliente</label>
                                        <select class="form-select" id="cliente" required>
                                            <option value="">Selecione uma cliente...</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="selectServico" class="form-label">Serviço (Predefinido)</label>
                                        <select class="form-select" id="selectServico" required onchange="atualizarDadosServico()">
                                            <option value="">Selecione um serviço...</option>
                                        </select>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label for="data" class="form-label">Data</label>
                                            <input type="date" class="form-control" id="data" required>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label for="hora" class="form-label">Hora</label>
                                            <input type="time" class="form-control" id="hora" required>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label for="valor" class="form-label">Valor (R$)</label>
                                        <input type="number" step="0.01" class="form-control" id="valor" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="pagamento" class="form-label">Forma de Pagamento</label>
                                        <select class="form-select" id="pagamento" required>
                                            <option value="PIX">PIX</option>
                                            <option value="Cartão de Crédito">Cartão de Crédito</option>
                                            <option value="Cartão de Débito">Cartão de Débito</option>
                                            <option value="Dinheiro">Dinheiro</option>
                                        </select>
                                    </div>
                                    <button type="submit" class="btn btn-success w-100"><i class="fa-solid fa-save"></i> Salvar Agendamento</button>
                                </form>
                            </div>
                        </div>
                    </div>

                    <!-- Lista de Agendamentos -->
                    <div class="col-md-8">
                        <div class="card shadow-sm">
                            <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                                <h5 class="mb-0"><i class="fa-solid fa-calendar-check"></i> Atendimentos Agendados</h5>
                                <span id="totalAgendamentos" class="badge bg-secondary">0 agendamentos</span>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped align-middle">
                                        <thead>
                                            <tr>
                                                <th>Data/Hora</th>
                                                <th>Cliente</th>
                                                <th>Serviço</th>
                                                <th>Valor</th>
                                                <th>Pagamento</th>
                                                <th>Ações</th>
                                            </tr>
                                        </thead>
                                        <tbody id="tabelaAgendamentos">
                                            <!-- Preenchido via JavaScript -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ABA 2: GERENCIAR CLIENTES -->
            <div class="tab-pane fade" id="clientes" role="tabpanel">
                <div class="row">
                    <!-- Cadastro / Edição de Cliente -->
                    <div class="col-md-4 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-header bg-info text-white">
                                <h5 class="mb-0" id="tituloFormCliente"><i class="fa-solid fa-user-plus"></i> Cadastrar Nova Cliente</h5>
                            </div>
                            <div class="card-body">
                                <form id="formCliente">
                                    <input type="hidden" id="editIndexCliente" value="">
                                    <div class="mb-3">
                                        <label for="nomeCliente" class="form-label">Nome da Cliente</label>
                                        <input type="text" class="form-control" id="nomeCliente" placeholder="Ex: Maria Silva" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="telefoneCliente" class="form-label">Telefone / WhatsApp</label>
                                        <input type="text" class="form-control" id="telefoneCliente" placeholder="Ex: (19) 99999-9999">
                                    </div>
                                    <div class="mb-3">
                                        <label for="obsCliente" class="form-label">Observações (Alergias / Preferências)</label>
                                        <textarea class="form-control" id="obsCliente" rows="2" placeholder="Ex: Prefere esmalte em gel vermelho"></textarea>
                                    </div>
                                    <button type="submit" class="btn btn-info text-white w-100" id="btnSalvarCliente"><i class="fa-solid fa-plus"></i> Adicionar Cliente</button>
                                    <button type="button" class="btn btn-secondary w-100 mt-2 d-none" id="btnCancelarCliente" onclick="cancelarEdicaoCliente()">Cancelar</button>
                                </form>
                            </div>
                        </div>
                    </div>

                    <!-- Lista de Clientes -->
                    <div class="col-md-8">
                        <div class="card shadow-sm">
                            <div class="card-header bg-dark text-white">
                                <h5 class="mb-0"><i class="fa-solid id-card"></i> Clientes Cadastradas</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped align-middle">
                                        <thead>
                                            <tr>
                                                <th>Nome</th>
                                                <th>Telefone</th>
                                                <th>Observações</th>
                                                <th>Ações</th>
                                            </tr>
                                        </thead>
                                        <tbody id="tabelaClientes">
                                            <!-- Preenchido via JavaScript -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ABA 3: GERENCIAR SERVIÇOS -->
            <div class="tab-pane fade" id="servicos" role="tabpanel">
                <div class="row">
                    <!-- Cadastro / Edição de Serviço -->
                    <div class="col-md-4 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-header bg-secondary text-white">
                                <h5 class="mb-0" id="tituloFormServico"><i class="fa-solid fa-scissors"></i> Cadastrar Novo Serviço</h5>
                            </div>
                            <div class="card-body">
                                <form id="formServico">
                                    <input type="hidden" id="editIndexServico" value="">
                                    <div class="mb-3">
                                        <label for="nomeServico" class="form-label">Nome do Serviço</label>
                                        <input type="text" class="form-control" id="nomeServico" placeholder="Ex: Esmaltação em Gel" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="precoServico" class="form-label">Preço Padrão (R$)</label>
                                        <input type="number" step="0.01" class="form-control" id="precoServico" placeholder="0.00" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="tempoServico" class="form-label">Duração Estimada</label>
                                        <input type="text" class="form-control" id="tempoServico" placeholder="Ex: 45 min" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary w-100" id="btnSalvarServico"><i class="fa-solid fa-plus"></i> Adicionar Serviço</button>
                                    <button type="button" class="btn btn-secondary w-100 mt-2 d-none" id="btnCancelarServico" onclick="cancelarEdicaoServico()">Cancelar</button>
                                </form>
                            </div>
                        </div>
                    </div>

                    <!-- Lista de Serviços Cadastrados -->
                    <div class="col-md-8">
                        <div class="card shadow-sm">
                            <div class="card-header bg-dark text-white">
                                <h5 class="mb-0"><i class="fa-solid fa-list"></i> Serviços Pré-definidos</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-striped align-middle">
                                        <thead>
                                            <tr>
                                                <th>Serviço</th>
                                                <th>Preço Padrão</th>
                                                <th>Duração</th>
                                                <th>Ações</th>
                                            </tr>
                                        </thead>
                                        <tbody id="tabelaServicos">
                                            <!-- Preenchido via JavaScript -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Script de Controle -->
    <script>
        let agendamentos = JSON.parse(localStorage.getItem('agendamentos')) || [];
        let servicos = JSON.parse(localStorage.getItem('servicos')) || [
            { nome: 'Manicure Simples', preco: 35.00, tempo: '30 min' },
            { nome: 'Esmaltação em Gel', preco: 60.00, tempo: '1 hora' },
            { nome: 'Alongamento em Fibra', preco: 150.00, tempo: '2 horas' }
        ];
        let clientes = JSON.parse(localStorage.getItem('clientes')) || [];

        if (!localStorage.getItem('servicos')) {
            localStorage.setItem('servicos', JSON.stringify(servicos));
        }

        // --- GERENCIAR CLIENTES ---
        function renderizarClientes() {
            const tbody = document.getElementById('tabelaClientes');
            tbody.innerHTML = '';
            
            clientes.forEach((c, index) => {
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${c.nome}</strong></td>
                        <td>${c.telefone || 'N/A'}</td>
                        <td><small class="text-muted">${c.obs || '-'}</small></td>
                        <td>
                            <button class="btn btn-warning btn-sm me-1" onclick="editarCliente(${index})" title="Editar">
                                <i class="fa-solid fa-pen text-white"></i>
                            </button>
                            <button class="btn btn-danger btn-sm" onclick="excluirCliente(${index})" title="Excluir">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            atualizarSelectClientes();
        }

        function atualizarSelectClientes() {
            const select = document.getElementById('cliente');
            select.innerHTML = '<option value="">Selecione uma cliente...</option>';
            clientes.forEach((c) => {
                select.innerHTML += `<option value="${c.nome}">${c.nome} (${c.telefone || 'Sem tel'})</option>`;
            });
        }

        document.getElementById('formCliente').addEventListener('submit', function(e) {
            e.preventDefault();
            const index = document.getElementById('editIndexCliente').value;
            const novaCliente = {
                nome: document.getElementById('nomeCliente').value,
                telefone: document.getElementById('telefoneCliente').value,
                obs: document.getElementById('obsCliente').value
            };

            if (index === "") {
                clientes.push(novaCliente);
            } else {
                clientes[index] = novaCliente;
                cancelarEdicaoCliente();
            }

            localStorage.setItem('clientes', JSON.stringify(clientes));
            document.getElementById('formCliente').reset();
            renderizarClientes();
        });

        function editarCliente(index) {
            const c = clientes[index];
            document.getElementById('nomeCliente').value = c.nome;
            document.getElementById('telefoneCliente').value = c.telefone;
            document.getElementById('obsCliente').value = c.obs;
            document.getElementById('editIndexCliente').value = index;

            document.getElementById('tituloFormCliente').innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Editar Cliente';
            document.getElementById('btnSalvarCliente').innerHTML = '<i class="fa-solid fa-save"></i> Atualizar Cliente';
            document.getElementById('btnCancelarCliente').classList.remove('d-none');
        }

        function cancelarEdicaoCliente() {
            document.getElementById('formCliente').reset();
            document.getElementById('editIndexCliente').value = "";
            document.getElementById('tituloFormCliente').innerHTML = '<i class="fa-solid fa-user-plus"></i> Cadastrar Nova Cliente';
            document.getElementById('btnSalvarCliente').innerHTML = '<i class="fa-solid fa-plus"></i> Adicionar Cliente';
            document.getElementById('btnCancelarCliente').classList.add('d-none');
        }

        function excluirCliente(index) {
            if (confirm('Deseja realmente excluir esta cliente?')) {
                clientes.splice(index, 1);
                localStorage.setItem('clientes', JSON.stringify(clientes));
                renderizarClientes();
            }
        }

        // --- GERENCIAR SERVIÇOS ---
        function renderizarServicos() {
            const tbody = document.getElementById('tabelaServicos');
            tbody.innerHTML = '';
            
            servicos.forEach((s, index) => {
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${s.nome}</strong></td>
                        <td>R$ ${parseFloat(s.preco).toFixed(2)}</td>
                        <td><span class="badge bg-info text-dark">${s.tempo}</span></td>
                        <td>
                            <button class="btn btn-warning btn-sm me-1" onclick="editarServico(${index})" title="Editar">
                                <i class="fa-solid fa-pen text-white"></i>
                            </button>
                            <button class="btn btn-danger btn-sm" onclick="excluirServico(${index})" title="Excluir">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            atualizarSelectServicos();
        }

        function atualizarSelectServicos() {
            const select = document.getElementById('selectServico');
            select.innerHTML = '<option value="">Selecione um serviço...</option>';
            servicos.forEach((s) => {
                select.innerHTML += `<option value="${s.nome}" data-preco="${s.preco}">${s.nome} - R$ ${parseFloat(s.preco).toFixed(2)} (${s.tempo})</option>`;
            });
        }

        function atualizarDadosServico() {
            const select = document.getElementById('selectServico');
            const selectedOption = select.options[select.selectedIndex];
            const preco = selectedOption.getAttribute('data-preco');
            if (preco) {
                document.getElementById('valor').value = preco;
            }
        }

        document.getElementById('formServico').addEventListener('submit', function(e) {
            e.preventDefault();
            const index = document.getElementById('editIndexServico').value;
            const novoServico = {
                nome: document.getElementById('nomeServico').value,
                preco: parseFloat(document.getElementById('precoServico').value),
                tempo: document.getElementById('tempoServico').value
            };

            if (index === "") {
                servicos.push(novoServico);
            } else {
                servicos[index] = novoServico;
                cancelarEdicaoServico();
            }

            localStorage.setItem('servicos', JSON.stringify(servicos));
            document.getElementById('formServico').reset();
            renderizarServicos();
        });

        function editarServico(index) {
            const s = servicos[index];
            document.getElementById('nomeServico').value = s.nome;
            document.getElementById('precoServico').value = s.preco;
            document.getElementById('tempoServico').value = s.tempo;
            document.getElementById('editIndexServico').value = index;

            document.getElementById('tituloFormServico').innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Editar Serviço';
            document.getElementById('btnSalvarServico').innerHTML = '<i class="fa-solid fa-save"></i> Atualizar Serviço';
            document.getElementById('btnCancelarServico').classList.remove('d-none');
        }

        function cancelarEdicaoServico() {
            document.getElementById('formServico').reset();
            document.getElementById('editIndexServico').value = "";
            document.getElementById('tituloFormServico').innerHTML = '<i class="fa-solid fa-scissors"></i> Cadastrar Novo Serviço';
            document.getElementById('btnSalvarServico').innerHTML = '<i class="fa-solid fa-plus"></i> Adicionar Serviço';
            document.getElementById('btnCancelarServico').classList.add('d-none');
        }

        function excluirServico(index) {
            if (confirm('Deseja realmente excluir este serviço?')) {
                servicos.splice(index, 1);
                localStorage.setItem('servicos', JSON.stringify(servicos));
                renderizarServicos();
            }
        }

        // --- GERENCIAR AGENDAMENTOS ---
        function renderizarAgendamentos() {
            const tbody = document.getElementById('tabelaAgendamentos');
            tbody.innerHTML = '';
            
            agendamentos.sort((a, b) => new Date(a.data + 'T' + a.hora) - new Date(b.data + 'T' + b.hora));

            agendamentos.forEach((ag, index) => {
                const partesData = ag.data ? ag.data.split('-') : ['', '', ''];
                const dataFormatada = partesData.length === 3 ? `${partesData[2]}/${partesData[1]}/${partesData[0]}` : ag.data;

                tbody.innerHTML += `
                    <tr>
                        <td><strong>${dataFormatada || ''}</strong><br><small class="text-muted">${ag.hora || ''}</small></td>
                        <td><strong>${ag.cliente || ''}</strong></td>
                        <td>${ag.servico || ''}</td>
                        <td>R$ ${parseFloat(ag.valor || 0).toFixed(2)}</td>
                        <td><span class="badge bg-success">${ag.pagamento || ''}</span></td>
                        <td>
                            <button class="btn btn-danger btn-sm" onclick="excluirAgendamento(${index})" title="Excluir">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
            document.getElementById('totalAgendamentos').innerText = `${agendamentos.length} agendamento(s)`;
        }

        document.getElementById('formAgendamento').addEventListener('submit', function(e) {
            e.preventDefault();
            const novoAg = {
                cliente: document.getElementById('cliente').value,
                servico: document.getElementById('selectServico').value,
                data: document.getElementById('data').value,
                hora: document.getElementById('hora').value,
                valor: document.getElementById('valor').value,
                pagamento: document.getElementById('pagamento').value
            };
            agendamentos.push(novoAg);
            localStorage.setItem('agendamentos', JSON.stringify(agendamentos));
            document.getElementById('formAgendamento').reset();
            renderizarAgendamentos();
        });

        function excluirAgendamento(index) {
            if (confirm('Deseja excluir este agendamento?')) {
                agendamentos.splice(index, 1);
                localStorage.setItem('agendamentos', JSON.stringify(agendamentos));
                renderizarAgendamentos();
            }
        }

        renderizarClientes();
        renderizarServicos();
        renderizarAgendamentos();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
