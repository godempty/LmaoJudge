function add_sample(){
    section = document.getElementById('io-sample');
    section.innerHTML += `<div class='io-f'><textarea type='text' class='form-control io-format samples' name='sample[]' `+   
    `placeholder='input sample ${section.children.length +1}'required></textarea><div class='io-f-space'></div><textarea type='text' class='form-control io-format samples'`+
    `name='sample[]'placeholder='output sample ${section.children.length +1}'required></textarea></div>`;
}
function del_sample(){
    section = document.getElementById('io-sample');
    last = section.lastElementChild;
    if(section.children.length > 1){
        section.removeChild(last);
    }
    else{
        alert(`you can't delete the last element of sample!`)
    }
}

function sol_answer(){
    section = document.getElementById('sol-block');
    section.innerHTML = "<textarea type='text'"+
    "class='form-control io-format samples'"+
    "name='solution-answer'"+
    "placeholder='solution-answer'"+
    "required"+
    "></textarea>";
}

function sol_code(){
    section = document.getElementById('sol-block');
    section.innerHTML = "<textarea type='text'"+
    "class='form-control io-format samples'"+
    "name='solution-code'"+
    "placeholder='solution-code'"+
    "required"+
    "></textarea>";
}