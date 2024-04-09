#include "addguestform.h"
#include "ui_addguestform.h"

#include "QDebug"

addGuestForm::addGuestForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::addGuestForm)
{
    ui->setupUi(this);

    this->ui->yearOfBirth->setValidator(new QIntValidator(1900, 2024));
}

addGuestForm::~addGuestForm()
{
    delete ui;
}

void addGuestForm::clear()
{
    this->ui->passport->clear();
    this->ui->fullName->clear();
    this->ui->yearOfBirth->clear();
    this->ui->address->clear();
    this->ui->reason->clear();
}

void addGuestForm::on_addGuestBtn_clicked()
{

    QString data = "addGuest;" + this->ui->passport->text() + ";" + this->ui->fullName->text() + ";" +
                   this->ui->yearOfBirth->text() + ";" + this->ui->address->text() + ";" + this->ui->reason->text();

    emit sendData(data);
}

