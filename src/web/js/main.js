(async function() {
    startChecker()
    initGUI()

    answer = await eel.ask_gigachat()()
    alert(answer)
})();