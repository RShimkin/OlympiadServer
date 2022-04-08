window.onload = function () {
    
    const curtitle = document.querySelector('#id_title').value
    const lang = document.querySelector('#id_plang').value
    //const ta = document.querySelector('#ta')
    const sb = document.querySelector('.sb')
    sb.addEventListener('click', (e) => {
        const form = document.forms[0]
        const fd = new FormData(form)
        console.log(fd)
        //ta.value = ta.value.replaceAll("\r","")
        e.preventDefault()

        document.querySelector('#ta').value = editor.getValue()

        $.ajax({
            data: $(form).serialize(), 
            type: 'POST', // GET or POST
            url: location.href,
            success: function (resp) {
                console.log("Получено")
                console.log(resp)
            },
            error: function (resp) {
                console.log("Ошибка")
                
            }
        })

        /*
        fetch(location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8' // x-www-form-urlencoded
            },
            body: JSON.stringify(data)
        }).then(resp => console.log(resp)) */
    })

    editor = CodeMirror.fromTextArea(document.getElementById("ta"), {
        styleActiveLine: true,
        lineNumbers: true,
        matchBrackets: true, 
        mode: 'text/x-c++src',
        indentUnit: 4,
        theme: 'dracula',
        scrollbarStyle: 'overlay'
        //value: "#include <iostream>\n\nusing namespace std\n\nint main(int argc, *char[] argv){\nreturn0\n};"
    }); 

    $('#id_plang').on('change', (e) => {
        //editor.setOption("mode", this.value)
    })
}

let editor