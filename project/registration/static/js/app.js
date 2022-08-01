$(document).ready(function() {
    $('#tariff').keyup(function(ev) {
        var total_incl_gst = $('#tariff').val() * 1;
        var total_excl_gst = Math.round(total_incl_gst / 1.12, 2);
        var gst = total_incl_gst - total_excl_gst;
        var gstobj = document.getElementById('gst');
        var exclobj = document.getElementById('tariff_wo_gst');
        gstobj.value = gst;
        exclobj.value = total_excl_gst;
    });

    $('#payment_mode').change(function(ev) {
        var mode = $('#payment_mode').val();
        console.log(mode);
        if (mode == 9){
            tpr = document.getElementById('tpr');
            tpr.value = 0;
            tpr.style.display = 'none';
            npa = document.getElementById('npa');
            npa.style.display = 'none';
            npa.value =  $('#tariff').val() * 1;
        }
        else{
            tpr = document.getElementById('tpr');
            tpr.style.display = 'block';
            npa = document.getElementById('npa');
            npa.style.display = 'block';
        }
    });

    $('#tpr').keyup(function(ev) {
        var total_incl_gst = $('#tariff').val() * 1;
        var net_payable = total_incl_gst - $('#tpr').val() * 1;
        var net_payable_obj = document.getElementById('npa');
        net_payable_obj.value = net_payable;
    });
});