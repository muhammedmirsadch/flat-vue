"""
URL configuration for flatvue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login_load/',views.login_load ),
    path('login_post/',views.login_post),




    path('admin_verify_flat_owner/',views.admin_verify_flat_owner ),
    path('admin_view_app_review/', views.admin_view_app_review),
    path('admin_view_facilities/', views.admin_view_facilities),
    path('admin_view_flat_details/', views.admin_view_flat_details),
    path('adminhome/', views.adminhome),
    path('admin_changepassword/', views.admin_changepassword),
    path('changepass_post/', views.changepass_post),

    path('flat_owner_add_broadcast_notification/<id>',views.flat_owner_add_broadcast_notification),
    path('addbrdcastnotif_post/',views.addbrdcastnotif_post),
    path('flat_owner_add_flat_occupants/', views.flat_owner_add_flat_occupants),
    path('addflatoccu_post/', views.addflatoccu_post),
    path('flat_owner_add_rent_or_payment/', views.flat_owner_add_rent_or_payment),
    path('flat_owner_add_security/', views.flat_owner_add_security),
    path('addsecurity_post/', views.addsecurity_post),
    path('flat_owner_add_facilities/', views.flat_owner_add_facilities),
    path('addfacilities_post/', views.addfacilities_post),
    path('flat_owner_manage_facilities/', views.flat_owner_manage_facilities),
    path('flat_owner_add_service_provider/', views.flat_owner_add_service_provider),
    path('flat_owner_add_surveillance_camera/', views.flat_owner_add_surveillance_camera),
    path('addsurvcamera_post/', views.addsurvcamera_post),
    path('flat_owner_assign_service_provider/', views.flat_owner_assign_service_provider),
    path('flat_owner_assign_work/<id>', views.flat_owner_assign_work),
    path('assignwork_post/', views.assignwork_post),
    path('flat_owner_complaint_reply/<id>', views.flat_owner_complaint_reply),
    path('flat_owner_complaint_reply_post/', views.flat_owner_complaint_reply_post),
    path('flat_owner_edit_flat_occupants/', views.flat_owner_edit_flat_occupants),
    path('editflatoccu_post/',views.editflatoccu_post),
    path('flat_owner_edit_security/<id>', views.flat_owner_edit_security),
    path('editsecurity_post/', views.editsecurity_post),
    path('flat_owner_edit_service_provider/<id>', views.flat_owner_edit_service_provider),
    path('editservprovider_post/',views.editservprovider_post),
    path('flat_owner_edit_cam/<id>', views.flat_owner_edit_cam),
    path('editcamera_post/', views.editcamera_post),
    path('flat_owner_delete_camera/<id>', views.flat_owner_delete_camera),
    path('flat_owner_manage_bd_notif/<id>', views.flat_owner_manage_bd_notif),
    path('flat_owner_delete_bdnotif/<id>', views.flat_owner_delete_bdnotif),
    path('flat_owner_manage_flat_occu/', views.flat_owner_manage_flat_occu),
    path('flat_owner_manage_rent/', views.flat_owner_manage_rent),
    path('addrentorpaym_post/', views.addrentorpaym_post),
    path('flat_owner_manage_security/', views.flat_owner_manage_security),
    path('flat_owner_manage_service_provider/', views.flat_owner_manage_service_provider),
    path('adddservprovi_post/',views.adddservprovi_post),
    path('flat_owner_manage_cam/', views.flat_owner_manage_cam),
    path('flat_owner_monitor_pay_status/', views.flat_owner_monitor_pay_status),
    path('flat_owner_reg_flat_owner/', views.flat_owner_reg_flat_owner),
    path('regflatowner_post/', views.regflatowner_post),
    path('flat_owner_service_req_reply/', views.flat_owner_service_req_reply),
    path('flat_owner_view_complaints/', views.flat_owner_view_complaints),
    path('flat_owner_view_service_req/', views.flat_owner_view_service_req),
    path('flat_owner_view_spot_notif/', views.flat_owner_view_spot_notif),
    path('flat_owner_view_entry_exit_log/', views.flat_owner_view_entry_exit_log),
    path('flat_owner_home/', views.flat_owner_home),
    path('logout/',views.logout),
    path('flat_owner_add_flat/',views.flat_owner_add_flat),
    path('addflat_post/',views.addflat_post),
    path('flat_owner_view_flat/',views.flat_owner_view_flat),
    path('admin_verify_flat_owner/',views.admin_verify_flat_owner),
    path('admin_approve_flat_owner/<id>/',views.admin_approve_flat_owner),
    path('admin_reject_flat_owner/<id>/',views.admin_reject_flat_owner),
    path('flat_owner_delet_flat/<id>',views.flat_owner_delet_flat),

    path('flat_owner_edit_flat/<id>',views.flat_owner_edit_flat),
    path('editflat_post/',views.editflat_post),

    path('flat_owner_delet_flat_occupant/<id>',views.flat_owner_delet_flat_occupant),
    path('flat_owner_edit_flat_occupant/<id>',views.flat_owner_edit_flat_occupant),
    path('editflatoccupant_post/',views.editflatoccupant_post),


    path('flat_owner_delete_service_provi/<id>',views.flat_owner_delete_service_provi),

    path('service_provider_home/', views.service_provider_home),
    path('service_provider_add_complaint/', views.service_provider_add_complaint),
    path('addcomplaint_post/', views.addcomplaint_post),
    path('service_provider_add_services/', views.service_provider_add_services),
    path('addservices_post/', views.addservices_post),
    path('service_provider_edit_services/<id>', views.service_provider_edit_services),
    path('editservices_post/', views.editservices_post),
    path('service_provider_delete_services/<id>', views.service_provider_delete_services),
    path('service_provider_manage_ongoing_services/', views.service_provider_manage_ongoing_services),
    path('service_provider_manage_services/', views.service_provider_manage_services),
    path('service_provider_update_ongoing_services/', views.service_provider_update_ongoing_services),
    path('service_provider_view_complaint/', views.service_provider_view_complaint),
    path('service_provider_view_service_req/', views.service_provider_view_service_req),
    path('delete_security/<id>', views.delete_security),
    path('service_provider_approve_servicerequest/<id>/', views.service_provider_approve_servicerequest),
    path('service_provider_reject_servicerequest/<id>/', views.service_provider_reject_servicerequest),


    ########################################flutter##########################################################

    path('LoginPostFlutter/', views.LoginPostFlutter),
    path('sendfeedback/', views.sendfeedback),
    path('Viewfeedback/', views.Viewfeedback),
    path('viewduty/', views.viewduty),
    path('viewnotification/', views.viewnotification),
    path('change_password_flutter/', views.change_password_flutter),


    path('flatoccupant_viewprofile/',views.flatoccupant_viewprofile),
    path('viewreply/',views.viewreply),
    path('sendcomplaint/',views.sendcomplaint),
    path('view_visitors/',views.view_visitors),
    path('view_notifications/',views.view_notifications),
    path('Add_visitor/',views.Add_visitor),
    path('BookCommonArea/',views.BookCommonArea),
    path('view_emergency_notification/',views.view_emergency_notification),
    path('send_emergency_notification/',views.send_emergency_notification),
    path('view_rent/',views.view_rent),
    path('monthly_rent_payment/',views.monthly_rent_payment),
    path('requestservices/',views.requestservices),
    path('viewservices/',views.viewservices),
    path('detect_noti/',views.detect_noti),




    path('security_viewprofile/',views.security_viewprofile),
    path('security_view_notification/',views.security_view_notification),
    path('security_change_password/',views.security_change_password),
    path('viewdutyschedule/',views.viewdutyschedule),
    path('update_status/',views.update_status),
    path('security_view_visitor/',views.security_view_visitor),
    path('send_service_request/',views.send_service_request),
    path('security_view_suspiciousactivity/', views.security_view_suspiciousactivity),

    path('mark_visitor/',views.mark_visitor),
    path('check_stranger_api/',views.check_stranger_api),
    path('ViewSuspiciosActivity/<id>',views.ViewSuspiciosActivity),

    path('forgotpasswordflutter/', views.forgotpasswordflutter),
    path('verifyOtpflutterPost/', views.verifyOtpflutterPost),
    path('changePasswordflutter/', views.changePasswordflutter),

    path('forgot_password/', views.forgot_password),
    path('forgotPassword_otp/', views.forgotPassword_otp),
    path('verifyOtp/', views.verifyOtp),
    path('verifyOtpPost/', views.verifyOtpPost),
    path('new_password/', views.new_password),
    path('changePassword/', views.changePassword),
    path('send_noti/', views.send_noti),

]
