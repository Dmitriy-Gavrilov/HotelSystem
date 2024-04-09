#ifndef FINDROOMBYIDFORM_H
#define FINDROOMBYIDFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class FindRoomByIdForm;
}

class FindRoomByIdForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit FindRoomByIdForm(QWidget *parent = nullptr);
    ~FindRoomByIdForm();

    void clear() override;

private slots:
    void on_FindRoomByIdBtn_clicked();

signals:
    void sendData(const QString &data);

private:
    Ui::FindRoomByIdForm *ui;
};

#endif // FINDROOMBYIDFORM_H
