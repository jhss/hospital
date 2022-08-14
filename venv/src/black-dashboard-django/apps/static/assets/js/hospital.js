var barChart;

function drawChart(asm) {
	var canvasElement = document.getElementById("barChart").getContext('2d');
	const _labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
					 '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', 
					 '22', '23'];
	const _names = ['뇌졸증', '고혈압', '혈액투석', '정신과', '수술부위 감염예방',
					'관상동맥우회술', '급성상기도감염 항생제 처방률',
					'주사제 처방률', '약품목수', '요양병원', '당뇨병', '대장암',
					'위암', '유방암', '폐암', '천식', '만성폐쇄성폐질환',
					'폐렴', '중환자실', '신생아중환자실', '마취', '정신건강 입원영역',
					'급성하기도감염 항생제 처방률'];
	
	var cars = document.getElementById('sido1');
	var wheel = document.getElementById('gugun1');
	console.log(cars.value);
	console.log(wheel.value);
	console.log("Hello");
    console.log("HEHEHEHEHE");
    console.log(asm);

	var new_label = [];
	var new_asm = [];
	for (let i = 0; i < _labels.length; i++){
		if (asm[i] != 0){
			new_label.push(_names[i]);
			new_asm.push(6 - asm[i]);
		}
	}

	var config = {
		type: "bar",
		data: {
			labels: new_label,
			datasets: [{ 
				label: "평가점수", 
				data: new_asm,
				backgroundColor: 'rgba(54, 162, 235, 0.6)', 
				borderColor: 'rgba(255, 99, 132, 0.6)',
				borderWidth: 1
			}],
		},
		options: {
			legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 13
                },
            },
			scaleShowValues: true,
			scales: {
				xAxes: [{
				  ticks: {
				  	fontColor: "white",
					autoSkip: false,
					padding: 14
				  },
				  gridLines: {
          			color: 'rgba(255,255,255,0.3)',
          			lineWidth: 1,
					drawTicks: false
       			  },

				}],
				yAxes: [{
					ticks: {
						fontColor: "white",
						beginAtZero: true,
						padding: 10,
					},
				  gridLines: {
          			color: 'rgba(255,255,255,0.3)',
          			lineWidth: 1,
					drawTicks: false
       			  },
        	    }],
                y : {
                    min: 0,
                    max: 5,
                }

			}
    	}
	};

	//var barChart = new Chart(canvasElement, config);


    if (window.bar != undefined) window.bar.destroy();
	window.bar = new Chart(canvasElement, config);
}

/*
//var ctx = document.getElementById("myChart");
var myChart = new Chart(canvasElement, {
    type: 'bar',
    data: {
        labels: ["Bill", "Jeff", "Micheal", "Tim", "Zuck"],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
            ],
        }]
    },
});
*/
