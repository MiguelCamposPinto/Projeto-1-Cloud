describe("Chat E2E", () => {

  const baseUrl = "http://localhost:8085/";

  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit(baseUrl);
  });

  it("carrega a página do chat", () => {
    cy.contains("💬 Chat").should("be.visible");
    cy.get("#name").should("exist");
    cy.get("#text").should("exist");
    cy.get("#send").should("exist");
    cy.get("#clearChat").should("exist");

    // Adiciona mensagem de teste concluído no chat
    cy.window().then((win) => {
      const chatEl = win.document.getElementById("chat");
      const div = win.document.createElement("div");
      div.className = "msg me";
      div.innerHTML = `<div><b>✅ Cypress</b></div><div>Teste "carrega a página do chat" concluído com sucesso!</div>`;
      chatEl.appendChild(div);
      chatEl.scrollTop = chatEl.scrollHeight; // rola para baixo
    });
  });

  it("define o nome e envia uma mensagem", () => {
    cy.get("#name").type("Tester");
    cy.get("#saveName").click();
    cy.get("#name").should("be.disabled");
    cy.get("#saveName").should("be.disabled");

    const msg = "Fim do teste de envio de mensagem.";
    cy.get("#text").type(msg);
    cy.get("#send").click();

    cy.contains(msg)
      .should("exist")
      .scrollIntoView()
      .should("be.visible");

    // Mensagem de teste concluído
    cy.window().then((win) => {
      const chatEl = win.document.getElementById("chat");
      const div = win.document.createElement("div");
      div.className = "msg me";
      div.innerHTML = `<div><b>Cypress</b></div><div>Teste concluído com sucesso!</div>`;
      chatEl.appendChild(div);
      chatEl.scrollTop = chatEl.scrollHeight;
    });
  });

  it("limpa o chat local", () => {
    cy.get("#name").type("Tester");
    cy.get("#saveName").click();
    cy.get("#text").type("FIM");
    cy.get("#send").click();

    cy.contains("FIM")
      .should("exist")
      .scrollIntoView();

    cy.get("#clearChat").click();
    cy.get("#chat").should("be.empty");

    // Mensagem de teste concluído
    cy.window().then((win) => {
      const chatEl = win.document.getElementById("chat");
      const div = win.document.createElement("div");
      div.className = "msg me";
      div.innerHTML = `<div><b>Cypress</b></div><div>Teste concluído com sucesso!</div>`;
      chatEl.appendChild(div);
      chatEl.scrollTop = chatEl.scrollHeight;
    });
  });

});
