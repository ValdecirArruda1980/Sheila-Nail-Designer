from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agenda - Sheila Nail Designer | Capivari</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome para Ícones -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-light">

    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-dark shadow-sm">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1"><i class="fa-solid fa-hand-sparkles text-pink me-2"></i> Sheila Nail Designer</span>
            <span class="text-white small"><i class="fa-solid fa-location-dot me-1"></i> Capivari - SP</span>
        </div>
    </nav>

    <div class="container my-4">
        <!-- Cards de Resumo -->
        <div class="row g-3 mb-4">
            <div class="col-md-4">
                <div class="card shadow-sm border-0 bg-white">
                    <div class="card-body">
                        <h6 class="text-muted mb-2">Agendamentos Hoje</h6>
                        <h3 id="totalAgendamentos" class="fw-bold text-primary">0</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card shadow-sm border-0 bg-white">
                    <div class="card-body">
                        <h6 class="text-muted mb-2">Faturamento Previsto</h6>
                        <h3 id="totalFaturamento" class="fw-bold text-success">R$ 0,00</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card shadow-sm border-0 bg-white">
                    <div class="card-body">
                        <h6 class="text-muted mb-2">Clientes Cadastrados</h6>
                        <h3 id="totalClientes" class="fw-bold text-info">0</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Abas de Navegação -->
        <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="pills-agenda-tab" data-bs-toggle="pill" data-bs-target="#pills-agenda" type="button" role="tab"><i class="fa-solid fa-calendar-days me-2"></i> Agenda</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="pills-clientes-tab" data-bs-toggle="pill" data-bs-target="#pills-clientes" type="button" role="tab"><i class="fa-solid fa-users me-2"></i> Clientes</button>
            </li>
        </ul>

        <div class="tab-content" id="pills-tabContent">
            <!-- ABA AGENDA -->
            <div class="tab-pane fade show active" id="pills-agenda" role="tabpanel">
                <div class="card shadow-sm border-0 mb-4">
                    <div class="card-header bg-white py-3">
                        <h5 class="mb-0 text-dark"><i class="fa-solid fa-plus-circle me-2 text-primary"></i> Novo Agendamento</h5>
                    </div>
                    <div class="card-body">
                        <form id="formAgendamento">
                            <div class="row g-3">
                                <div class="col-md-3">
                                    <label class="form-label">Cliente</label>
                                    <select class="form-select" id="agCliente" required>
                                        <option value="">Selecione a cliente...</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">Serviço</label>
                                    <input type="text" class="form-control" id="agServico" placeholder="Ex: Fibra de Vidro" required>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">Data</label>
                                    <input type="date" class="form-control" id="agData" required>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">Hora</label>
                                    <input type="time" class="form-control" id="agHora" required>
                                </div>
                                <div class="col-md-2">
                                    <label class="form-label">Valor (R$)</label>
                                    <input type="number" step="0.01" class="form-control" id="agValor" placeholder="0,00" required>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">Pagamento</label>
                                    <select class="form-select" id="agPagamento" required>
                                        <option value="PIX">PIX</option>
                                        <option value="Cartão de Crédito">Cartão de Crédito</option>
                                        <option value="Cartão de Débito">Cartão de Débito</option>
                                        <option value="Dinheiro">Dinheiro</option>
                                    </select>
                                </div>
                                <div class="col-md-9 d-flex align-items-end justify-content-end">
                                    <button type="submit" class="btn btn-primary px-4"><i class="fa-solid fa-check me-1"></i> Salvar Agendamento</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Lista de Agendamentos -->
                <div class="card shadow-sm border-0">
                    <div class="card-header bg-white py-3">
                        <h5 class="mb-0 text-dark"><i class="fa-solid fa-list me-2 text-primary"></i> Lista de Horários</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0 align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>Data</th>
                                        <th>Hora</th>
                                        <th>Cliente</th>
                                        <th>Serviço</th>
                                        <th>Valor</th>
                                        <th>Pagamento</th>
                                        <th>Status</th>
                                        <th class="text-end">Ações</th>
                                    </tr>
                                </thead>
                                <tbody id="tabelaAgendamentos">
                                    <!-- Preenchido via JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ABA CLIENTES -->
            <div class="tab-pane fade" id="pills-clientes" role="tabpanel">
                <div class="card shadow-sm border-0 mb-4">
                    <div class="card-header bg-white py-3">
                        <h5 class="mb-0 text-dark"><i class="fa-solid fa-user-plus me-2 text-info"></i> Cadastrar Nova Cliente</h5>
                    </div>
                    <div class="card-body">
                        <form id="formCliente">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <label class="form-label">Nome Completo</label>
                                    <input type="text" class="form-control" id="cliNome" placeholder="Nome da cliente" required>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">Telefone / WhatsApp</label>
                                    <input type="text" class="form-control" id="cliTelefone" placeholder="(19) 99999-9999" required>
                                </div>
                                <div class="col-md-3">
                                    <label class="form-label">Observações (Alergias / Preferências)</label>
                                    <input type="text" class="form-control" id="cliObs" placeholder="Ex: Alérgica a esmalte comum">
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button type="submit" class="btn btn-info text-white w-100"><i class="fa-solid fa-user-check me-1"></i> Cadastrar</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Lista de Clientes -->
                <div class="card shadow-sm border-0">
                    <div class="card-header bg-white py-3">
                        <h5 class="mb-0 text-dark"><i class="fa-solid fa-address-book me-2 text-info"></i> Clientes Cadastradas</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0 align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>Nome</th>
                                        <th>Telefone</th>
                                        <th>Observações</th>
                                        <th class="text-end">Ações</th>
                                    </tr>
                                </thead>
                                <tbody id="tabelaClientes">
                                    <!-- Preenchido via JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Script da Aplicação -->
    <script>
        let clientes = JSON.parse(localStorage.getItem('nail_clientes')) || [];
        let agendamentos = JSON.parse(localStorage.getItem('nail_agendamentos')) || [];

        function salvarDados() {
            localStorage.setItem('nail_clientes', JSON.stringify(clientes));
            localStorage.setItem('nail_agendamentos', JSON.stringify(agendamentos));
            atualizarTabelas();
        }

        function atualizarSelectClientes() {
            const select = document.getElementById('agCliente');
            select.innerHTML = '<option value="">Selecione a cliente...</option>';
            clientes.forEach(c => {
                select.innerHTML += `<option value="${c.nome}">${c.nome}</option>`;
            });
        }

        function atualizarTabelas() {
            const tbodyCli = document.getElementById('tabelaClientes');
            tbodyCli.innerHTML = '';
            
            if (clientes.length === 0) {
                tbodyCli.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-3">Nenhuma cliente cadastrada ainda.</td></tr>`;
            } else {
                clientes.forEach((c, index) => {
                    tbodyCli.innerHTML += `
                        <tr>
                            <td class="fw-semibold">${c.nome}</td>
                            <td>${c.telefone}</td>
                            <td><span class="badge bg-warning text-dark">${c.obs || 'Nenhuma'}</span></td>
                            <td class="text-end">
                                <button class="btn btn-sm btn-outline-danger" onclick="removerCliente(${index})"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                    `;
                });
            }

            const tbodyAg = document.getElementById('tabelaAgendamentos');
            tbodyAg.innerHTML = '';
            let faturamentoTotal = 0;

            if (agendamentos.length === 0) {
                tbodyAg.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-3">Nenhum agendamento registrado ainda.</td></tr>`;
            } else {
                agendamentos.forEach((a, index) => {
                    if(a.status === 'Concluído') {
                        faturamentoTotal += parseFloat(a.valor);
                    }
                    
                    let dataPartes = a.data ? a.data.split('-') : ['', '', ''];
                    let dataFormatada = dataPartes.length === 3 ? `${dataPartes[2]}/${dataPartes[1]}/${dataPartes[0]}` : a.data;
                    
                    let badgeStatus = a.status === 'Concluído' ? 'bg-success' : 'bg-primary';

                    tbodyAg.innerHTML += `
                        <tr>
                            <td>${dataFormatada}</td>
                            <td class="fw-bold text-primary">${a.hora}</td>
                            <td class="fw-semibold">${a.cliente}</td>
                            <td>${a.servico}</td>
                            <td>R$ ${parseFloat(a.valor).toFixed(2)}</td>
                            <td><span class="badge bg-secondary">${a.pagamento || 'PIX'}</span></td>
                            <td><span class="badge ${badgeStatus}">${a.status}</span></td>
                            <td class="text-end">
                                <button class="btn btn-sm btn-outline-success me-1" onclick="alternarStatus(${index})" title="Alternar Status"><i class="fa-solid fa-check"></i></button>
                                <button class="btn btn-sm btn-outline-danger" onclick="removerAgendamento(${index})" title="Excluir"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                    `;
                });
            }

            document.getElementById('totalAgendamentos').innerText = agendamentos.length;
            document.getElementById('totalFaturamento').innerText = `R$ ${faturamentoTotal.toFixed(2)}`;
            document.getElementById('totalClientes').innerText = clientes.length;

            atualizarSelectClientes();
        }

        document.getElementById('formCliente').addEventListener('submit', function(e) {
            e.preventDefault();
            const novaCliente = {
                id: Date.now(),
                nome: document.getElementById('cliNome').value,
                telefone: document.getElementById('cliTelefone').value,
                obs: document.getElementById('cliObs').value
            };
            clientes.push(novaCliente);
            salvarDados();
            this.reset();
        });

        document.getElementById('formAgendamento').addEventListener('submit', function(e) {
            e.preventDefault();
            const novoAg = {
                id: Date.now(),
                cliente: document.getElementById('agCliente').value,
                servico: document.getElementById('agServico').value,
                data: document.getElementById('agData').value,
                hora: document.getElementById('agHora').value,
                valor: parseFloat(document.getElementById('agValor').value),
                pagamento: document.getElementById('agPagamento').value,
                status: 'Agendado'
            };
            agendamentos.push(novoAg);
            salvarDados();
            this.reset();
        });

        function removerCliente(index) {
            if(confirm('Deseja realmente excluir esta cliente?')) {
                clientes.splice(index, 1);
                salvarDados();
            }
        }

        function removerAgendamento(index) {
            if(confirm('Deseja realmente excluir este agendamento?')) {
                agendamentos.splice(index, 1);
                salvarDados();
            }
        }

        function alternarStatus(index) {
            agendamentos[index].status = agendamentos[index].status === 'Agendado' ? 'Concluído' : 'Agendado';
            salvarDados();
        }

        atualizarTabelas();
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
