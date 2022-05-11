$(document).ready(function () {
    let admin_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OCwiZW1haWwiOiJhZG1pbkB5YW5kZXgucnUiLCJzYWx0IjoiclJiRm51SyJ9.Uh6DxheYOQRCVkoB2CbWmmln-JDXWy12MeR2N_fAcSY'
    let acer_manufacturer_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwiZW1haWwiOiJhY2VyQHlhbmRleC5ydSIsInNhbHQiOiJjRTdWczgzIn0.k54eMtVxtACzaeqEr67kpspf1aNwhbyJF-wjzLWHo5w';
    let asus_manufacturer_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJyeWJraW4uZ2Vvcmd5QHlhbmRleC5ydSIsInNhbHQiOiJtTHdFVkZxIn0.SJofJ17u0BhPjLdanGjmyqaVmKjfk7FkskBMtwsyqHs';
    let asus_service_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZW1haWwiOiJhc3Vzc2VydmljZUB5YW5kZXgucnUiLCJzYWx0IjoiWWx0T2k2dSJ9.72AgVvj6_W6el0M4LKml1D6HFywhiaMCK8ij8Pu_0wE';
    let current_token = '';
    let user_type = 0;

    function fetchBlob(uri, token, callback) {
      let xhr = new XMLHttpRequest();
      xhr.open('GET', uri, true);
      xhr.setRequestHeader('Authorization', token);
      xhr.responseType = 'arraybuffer';

      xhr.onload = function(e) {
        if (this.status === 200) {
          let blob = this.response;
          if (callback) {
            callback(blob);
          }
        }
      };
      xhr.send();
    }

    $('.user').change(function () {
        document.getElementById('admin').style.display = 'none';
        document.getElementById('manufacturer').style.display = 'none';
        document.getElementById('service').style.display = 'none';
        let selector_val = $(this).val();
        if (selector_val === '1') {
            current_token = admin_token;
            user_type = 1;
        } else if (selector_val === '2') {
            current_token = asus_manufacturer_token;
            user_type = 2;
        } else if (selector_val === '3') {
            current_token = acer_manufacturer_token;
            user_type = 2;
        } else if (selector_val === '4') {
            current_token = asus_service_token;
            user_type = 3;
        }

        if (user_type === 1) {
            document.getElementById('admin').style.display = 'block';
            $('#manufacturers').empty();

            // СОЗДАНИЕ ПРОИЗВОДИТЕЛЯ
            $('.create_manufacturer').click(function () {
               let send_data = new FormData();
                 send_data.append('name', $('#manufacturer_name').val());

                 let req = $.ajax({
                     url: '/api/manufacturers/create',
                     type: 'POST',
                     data: send_data,
                     enctype: 'multipart/form-data',
                     processData: false,
                     contentType: false,
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         alert('Производитель был создан!');
                     } else {
                         alert('Произошла ошибка!');
                     }
                 })
            });


            // ВЫВОД СОЗДАННЫХ ПРОИЗВОДИТЕЛЕЙ
            let req = $.ajax({
                     url: '/api/manufacturers',
                     type: 'GET',
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         let manufacturers = data.data;
                         manufacturers.forEach(manufacturer => {
                             let card_title = manufacturer.name;
                             $('#manufacturers').append(`
                                <div class="col">
                                    <div class="card h-100">
                                      <div class="card-body">
                                        <h5 class="card-title">${card_title}</h5>
                                      </div>
                                    </div>
                                  </div>
                            `)
                         })
                     }
                 })

        } else if (user_type === 2) {
            document.getElementById('manufacturer').style.display = 'block';
            $('#units').empty();
            $('#service_centers').empty();

            // СОЗДАНИЕ ТИПА МОДЕЛИ
            $('.create_model_type').click(function () {
               let send_data = new FormData();
                 send_data.append('name', $('#type_name').val());
                 send_data.append('warranty_period', $('#warranty_period').val());

                 let req = $.ajax({
                     url: '/api/products/types/create',
                     type: 'POST',
                     data: send_data,
                     enctype: 'multipart/form-data',
                     processData: false,
                     contentType: false,
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         alert('Тип модели был создан!');
                     } else {
                         alert('Произошла ошибка!');
                     }
                 })
            });



            // СОЗДАНИЕ МОДЕЛИ
            let model_type = null;
             $('.select_model_type').click(function () {
                 let req = $.ajax({
                     url: '/api/products/types',
                     type: 'GET',
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         let types = data.data;
                         $('#drop_model_type').empty();
                         types.forEach(item => {
                             $('#drop_model_type').append(`<a class="dropdown-item drop_model_type_item" id=${item.id} href="#">${item.name}</a>`);
                         });
                     }
                 })
             })
            $('#drop_model_type').on('click', '.drop_model_type_item', function (e) {
                $('#drop_model_type_text').text($(this).text());
                model_type = parseInt($(this).attr('id'));
            });
             
             $('.create_model').click(function () {
                 let send_data = new FormData();
                 send_data.append('model_name', $('#model_name').val());
                 send_data.append('product_type_id', model_type);
                 send_data.append('photo', $('#model_file')[0].files[0]);

                 let req = $.ajax({
                     url: '/api/products/models/create',
                     type: 'POST',
                     data: send_data,
                     enctype: 'multipart/form-data',
                     processData: false,
                     contentType: false,
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         alert('Модель была создана!');
                     } else {
                         alert('Произошла ошибка!');
                     }
                 })
             });




             // СОЗДАНИЕ ЕДИНИЦЫ ТЕХНИКИ
            let model = null;
             $('.select_model').click(function () {
                 let req = $.ajax({
                     url: '/api/products/models',
                     type: 'GET',
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         let types = data.data;
                         $('#drop_model').empty();
                         types.forEach(item => {
                             $('#drop_model').append(`<a class="dropdown-item drop_model_item" id=${item.id} href="#">${item.name}</a>`);
                         });
                     }
                 })
             })
            $('#drop_model').on('click', '.drop_model_item', function (e) {
                $('#drop_model_text').text($(this).text());
                model = parseInt($(this).attr('id'));
            });

             $('.create_unit').click(function () {
                 let send_data = new FormData();
                 send_data.append('model_id', model);
                 send_data.append('serial_number', $('#serial_number').val());

                 let req = $.ajax({
                     url: '/api/products/units/create',
                     type: 'POST',
                     data: send_data,
                     enctype: 'multipart/form-data',
                     processData: false,
                     contentType: false,
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         alert('Единица техники была создана!');
                     } else {
                         alert('Произошла ошибка!');
                     }
                 })
             });




             // СОЗДАНИЕ СЕРВИСНОГО ЦЕНТРА
             $('.create_service_center').click(function () {
                 let send_data = new FormData();
                 send_data.append('name', $('#service_center_name').val());
                 send_data.append('latitude', $('#service_latitude').val());
                 send_data.append('longitude', $('#service_longitude').val());
                 send_data.append('address', $('#service_address').val())
                 console.log(send_data);
                 let req = $.ajax({
                     url: '/api/serviceCenter/create',
                     type: 'POST',
                     data: send_data,
                     enctype: 'multipart/form-data',
                     processData: false,
                     contentType: false,
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req.done(function (data) {
                     if (data.status === 'ok') {
                         alert('Сервисный центр был создан!');
                     } else {
                         alert('Произошла ошибка!');
                     }
                 })
             });






             // ВЫВОД СОЗДАННЫХ ЕДИНИЦ ТЕХНИКИ
            let req1 = $.ajax({
                     url: '/api/products/units',
                     type: 'GET',
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req1.done(function (data) {
                     if (data.status === 'ok') {
                         let units = data.data;
                         units.forEach(unit => {
                             let card_title = unit.manufacturer + ' ' + unit.model;
                             let serial_number = unit.serialNumber;
                             let assigned = 'Не куплено';
                             if (unit.assigned) {
                                 assigned = 'Куплено';
                             }
                             $('#units').append(`
                                <div class="col">
                                    <div class="card h-100">
                                      <img src="" class="card-img-top unit_photo_${unit.id}">
                                      <div class="card-body">
                                        <h5 class="card-title">${card_title}</h5>
                                        <p class="card-text">Серийный номер: ${serial_number}<br> ${assigned}</p>
                                      </div>
                                    </div>
                                  </div>
                            `)
                             fetchBlob(unit.qrImage, current_token, function (blob) {
                                 let photo_b64 = btoa(String.fromCharCode.apply(null, new Uint8Array(blob)));
                                 $('.unit_photo_'+unit.id).attr('src', 'data:image/jpeg;base64,' + photo_b64);
                             })
                         })
                     }
                 })





            // ВЫВОД СОЗДАННЫХ СЕРВИСНЫХ ЦЕНТРОВ
            let req2 = $.ajax({
                     url: '/api/serviceCenter',
                     type: 'GET',
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
                 req2.done(function (data) {
                     if (data.status === 'ok') {
                         let service_centers = data.data;
                         service_centers.forEach(service_center => {
                             let card_title = service_center.name;
                             let address = service_center.address;
                             let coordinates = service_center.coordinates.join(', ');
                             $('#service_centers').append(`
                                <div class="col">
                                    <div class="card h-100">
                                      <div class="card-body">
                                        <h5 class="card-title">${card_title}</h5>
                                        <p class="card-text">Адрес: ${address}<br> Координаты: ${coordinates}</p>
                                      </div>
                                    </div>
                                  </div>
                            `)
                         })
                     }
                 })




        } else if (user_type === 3) {
            document.getElementById('service').style.display = 'block';
            $('#warranty_claims').empty();


            // ВЫВОД ТЕКУЩИХ ЗАЯВОК НА ГАРАНТИЙНОЕ ОБСЛУЖИВАНИЕ
            let req1 = $.ajax({
                     url: '/api/warrantyClaim',
                     type: 'GET',
                     beforeSend: function (xhr) {
                         xhr.setRequestHeader('Authorization', current_token);
                     }
                });
             req1.done(function (data) {
                 if (data.status === 'ok') {
                     let warranty_claims = data.data;
                     warranty_claims.forEach(claim => {
                         let card_title = claim.name;
                         let serial_number = claim.serialNumber;
                         let status = claim.status;
                         let problem = claim.problem;
                         $('#warranty_claims').append(`
                            <div class="col">
                                <div class="card h-100">
                                  <div class="card-body">
                                    <h5 class="card-title">${card_title}</h5>
                                    <p class="card-text">Серийный номер: ${serial_number}<br> 
                                    Проблема: ${problem}<br>
                                    Статус: ${status}
                                    </p>
                                    <button type="button" class="btn btn-primary open_modal" data-bs-toggle="modal" data-bs-target="#claim_modal" id=${claim.id}>
                                      Изменить статус
                                    </button>
                                  </div>
                                </div>
                              </div>
                        `)
                     })

                     // ЗАДАНИЕ НОВОГО СТАТУСА
                     $('#claim_modal').on('show.bs.modal', function (e) {
                         let claim_id = e.relatedTarget.id;

                         $('.change_claim').click(function () {
                             let send_data = new FormData();
                         send_data.append('claim_id', claim_id);
                         send_data.append('status', $('#new_claim_status').val());
                         let req = $.ajax({
                             url: '/api/warrantyClaim/status/change',
                             type: 'POST',
                             data: send_data,
                             enctype: 'multipart/form-data',
                             processData: false,
                             contentType: false,
                             beforeSend: function (xhr) {
                                 xhr.setRequestHeader('Authorization', current_token);
                             }
                        });
                         req.done(function (data) {
                             if (data.status === 'ok') {
                                 alert('Статус был изменен!');
                             } else {
                                 alert('Произошла ошибка!');
                             }
                         })
                         });

                     })
                 }
             })
        }
    })

})
