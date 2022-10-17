var curi = 0
var curj = 0

function newdata(ret){
	while(curi < ret.subtask.length){
		curj = 0
		while(curj < ret.subtask[curi].length){
			if(ret.subtask[curi][curj][0] != ""){
				$('#tk'+String(curi+curj))
				//const info = document.getElementById('tk' + String(curi+curj))
				//info.childNodes[3].innerText = ret.subtask[curi][curj][0]
				//info.childNodes[5].innerText = ret.subtask[curi][curj][1] + " ms"
				//info.childNodes[7].innerText = ret.subtask[curi][curj][2] + " kb"
				curj += 1
			}
			else break
		}
		if(curj >= ret.subtask[curi].length) curi += 1
		else break
	}
	if(ret.done == 1){
		verd.innerText = ret.verdict
		// colors for different results
		const color = document.getElementById('colorhead')
		if(ret.verdict == 'compile error'){
			for(let i=0;i<ret.subtask.length;++i) for(let j=0;j<ret.subtask[i].length;++j){
				const info = document.getElementById('tk' + String(i + j))
				info.childNodes[3].innerText = 'CE'
			}
			color.style = 'background-color: lightgoldenrodyellow'
		}
		else if(ret.verdict == 'AC') color.style = 'background-color: palegreen'
		else if(ret.verdict == 'WA') color.style = 'background-color: #ebccd1'
		else if(ret.verdict == 'TLE') color.style = 'background-color: lightsteelblue'
		return 0
	}
	return 1
}

$(document).ready(function(){
	var upd = setInterval(function(){
		$.ajax({
			url: window.location.href+'/get_data',
			type: 'get',
			dataType: 'json',
			success: function(response){
				alert(123)
				clearInterval(upd)
			},
			error: function(thrownError){
				console.log(thrownError)
				clearInterval(upd)
			}
		})
	}, 500)
})
