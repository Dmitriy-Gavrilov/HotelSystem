#include "deleteguestform.h"
#include "ui_deleteguestform.h"

DeleteGuestForm::DeleteGuestForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DeleteGuestForm)
{
    ui->setupUi(this);
}

DeleteGuestForm::~DeleteGuestForm()
{
    delete ui;
}

void DeleteGuestForm::clear()
{
    this->ui->passport->clear();
}

void DeleteGuestForm::on_deleteGuestBtn_clicked()
{
    QString data = "deleteGuest;" + this->ui->passport->text();
    emit sendData(data);
}

